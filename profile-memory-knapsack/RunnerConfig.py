from EventManager.Models.RunnerEvents import RunnerEvents
from EventManager.EventSubscriptionController import EventSubscriptionController
from ConfigValidator.Config.Models.RunTableModel import RunTableModel
from ConfigValidator.Config.Models.FactorModel import FactorModel
from ConfigValidator.Config.Models.RunnerContext import RunnerContext
from ConfigValidator.Config.Models.OperationType import OperationType
from ProgressManager.Output.OutputProcedure import OutputProcedure as output
from typing import Dict, List, Any, Optional
from pathlib import Path
from os.path import dirname, realpath
import numpy as np
import sys
import os
import signal
import pandas as pd
import time
import subprocess
import shlex
import textwrap
import re
import math

class RunnerConfig:
    ROOT_DIR = Path(dirname(realpath(__file__)))

    # ================================ USER SPECIFIC CONFIG ================================
    """The name of the experiment."""
    name:                       str             = "knapsack_experiment"
    """target function location in remote laptop"""
    target_function_location = 'memory.knapsack'
    target_function_names = ['knapsack_basic', 'knapsack_cache', 'knapsack_lru_cache']
    input_size_options = [
        (tuple([3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31]),
         tuple([10, 25, 35, 45, 60, 75, 85, 95, 110, 125, 140, 155, 165, 180, 195]), 50),
        (tuple([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]),
         tuple([15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300]), 75),
        (tuple([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49]), tuple(
            [5, 20, 35, 50, 65, 80, 95, 110, 125, 140, 155, 170, 185, 200, 215, 230, 245, 260, 275, 290, 305, 320, 335,
             350, 365]), 100)
    ]
    input_description = ["5 items, 10 capacity", "8 items, 15 capacity", "11 items, 20 capacity"]
    sampling_rate_options = [200]
    """The time Experiment Runner will wait after a run completes.
    This can be essential to accommodate for cooldown periods on some systems."""
    time_between_runs_in_ms:    int             = 60000 # should be 60000, 1minute

    """The path in which Experiment Runner will create a folder with the name `self.name`, in order to store the
    results from this experiment. (Path does not need to exist - it will be created if necessary.)
    Output path defaults to the config file's path, inside the folder 'experiments'"""
    results_output_path:        Path             = ROOT_DIR / 'experiments'

    """Experiment operation type. Unless you manually want to initiate each run, use `OperationType.AUTO`."""
    operation_type:             OperationType   = OperationType.AUTO

    """remote ssh connection details"""
    remote_user:                str             = "rr"
    remote_host: str = "192.168.0.104"

    """remote path to the experiment"""
    remote_package_dir:        str             = "/Users/rr/GreenLab/ProjectCode/profiling-using-exp-runner/packages"
    remote_temporary_results_dir:        str             = "/Users/rr/GreenLab/ProjectCode/profiling-using-exp-runner/RESULTS"

    """energibridge location in remote laptop"""
    energibridge_location:        str             = "/usr/local/bin/energibridge"
    """python location in remote laptop"""
    remote_python_location:        str             = "/Users/rr/anaconda3/bin/python"
    # Dynamic configurations can be one-time satisfied here before the program takes the config as-is
    # e.g. Setting some variable based on some criteria
    def __init__(self):
        """Executes immediately after program start, on config load"""
        EventSubscriptionController.subscribe_to_multiple_events([
            (RunnerEvents.BEFORE_EXPERIMENT, self.before_experiment),
            (RunnerEvents.BEFORE_RUN       , self.before_run       ),
            (RunnerEvents.START_RUN        , self.start_run        ),
            (RunnerEvents.START_MEASUREMENT, self.start_measurement),
            (RunnerEvents.INTERACT         , self.interact         ),
            (RunnerEvents.STOP_MEASUREMENT , self.stop_measurement ),
            (RunnerEvents.STOP_RUN         , self.stop_run         ),
            (RunnerEvents.POPULATE_RUN_DATA, self.populate_run_data),
            (RunnerEvents.AFTER_EXPERIMENT , self.after_experiment )
        ])
        self.run_table_model = None  # Initialized later
        output.console_log("Custom config loaded")

    def create_run_table_model(self) -> RunTableModel:
        """Create and return the run_table model here. A run_table is a List (rows) of tuples (columns),
        representing each run performed"""
        sampling_factor = FactorModel("sampling_rate", self.sampling_rate_options) # Define different sampling intervals
        input_size_factor = FactorModel("input_size", self.input_size_options)  # Define different input sizes
        cache_factor = FactorModel("cache_strategy", self.target_function_names)  # Different cache strategies
        self.run_table_model = RunTableModel(
            factors=[input_size_factor, sampling_factor, cache_factor],
            data_columns=['input_description', 'execution_time','execution_time_1', 'execution_time_2','average_cpu_usage','memory_usage','energy_consumption', 'dram_energy', 'package_energy', 'pp0_energy', 'pp1_energy']
        )
        return self.run_table_model

    def before_experiment(self) -> None:
        """Perform any activity required before starting the experiment here
        Invoked only once during the lifetime of the program."""

        remote_experiment_result_dir = f"{self.remote_temporary_results_dir}/{self.name}"
        ssh_cmd = f"ssh {self.remote_user}@{self.remote_host} 'mkdir -p {remote_experiment_result_dir}'"
        try:
            subprocess.run(shlex.split(ssh_cmd), check=True)
            output.console_log(f"Created remote directory: {remote_experiment_result_dir}")
        except subprocess.CalledProcessError as e:
            output.console_log(f"Error creating remote directory: {e}")
            raise e

    def before_run(self) -> None:
        """Perform any activity required before starting a run.
        No context is available here as the run is not yet active (BEFORE RUN)"""
        # packages_dir = os.path.join(self.ROOT_DIR, 'packages')
        pass

    def start_run(self, context: RunnerContext) -> None:
        """Perform any activity required for starting the run here.
        For example, starting the target system to measure.
        Activities after starting the run should also be performed here."""
        """Perform any activity required for starting the run here."""
        remote_temporary_each_run_results_dir = f"{self.remote_temporary_results_dir}/{self.name}/run_{context.run_nr}"
        ssh_cmd = f"ssh {self.remote_user}@{self.remote_host} 'mkdir -p {remote_temporary_each_run_results_dir}'"
        try:
            subprocess.run(shlex.split(ssh_cmd), check=True)
            output.console_log(f"Created remote run directory: {remote_temporary_each_run_results_dir}")
        except subprocess.CalledProcessError as e:
            output.console_log(f"Error creating remote run directory: {e}")
            raise e


    def start_measurement(self, context: RunnerContext) -> None:
        """Start energy measurement using Energibridge."""
        sampling_interval = context.run_variation['sampling_rate']
        target_function = context.run_variation['cache_strategy']
        input_size = context.run_variation['input_size']

        remote_temporary_each_run_results_dir = f"{self.remote_temporary_results_dir}/{self.name}/run_{context.run_nr}"
        python_cmd = (
            f"import sys; import os; import numpy as np; import time;"
            f"sys.path.append(\\\"{self.remote_package_dir}\\\"); "
            f"import {self.target_function_location} as module; "
            f"weights = {input_size[0]}; "
            f"values = {input_size[1]}; "
            f"capacity = {input_size[2]}; "
            f"start_time_1 = time.perf_counter(); "
            f"module.{target_function}(weights, values, capacity); "
            f"end_time_1 = time.perf_counter(); "
            f"execution_time_1 = end_time_1 - start_time_1; "
            f"print(f\\\"first call executed successfully\\\"); "
            f"print(f\\\"first call execution time: {{execution_time_1}} seconds\\\"); "   
            f"start_time_2 = time.perf_counter(); "
            f"module.{target_function}(weights, values, capacity); "
            f"end_time_2 = time.perf_counter(); "
            f"execution_time_2 = end_time_2 - start_time_2; "
            f"print(f\\\"second call executed successfully\\\"); "
            f"print(f\\\"second call execution time: {{execution_time_2}} seconds\\\"); "
            f"total_time = end_time_2 - start_time_1; "
            f"print(f\\\"Total execution time: {{total_time}} seconds\\\");"
        )

        profiler_cmd = (
            f"{self.energibridge_location} --interval {sampling_interval} "
            f"--max-execution 20 "
            f"--output {remote_temporary_each_run_results_dir}/energibridge.csv "
            f"--summary "
            f"{self.remote_python_location} -c '{python_cmd}' "
        )

        ssh_cmd = f'ssh {self.remote_user}@{self.remote_host} "{profiler_cmd}" '

        output.console_log(f"Executing Command:{ssh_cmd}")

        energibridge_log = open(f'{context.run_dir}/energibridge.log', 'w')

        self.profiler = subprocess.Popen(ssh_cmd, shell=True, stdout=energibridge_log, stderr=energibridge_log)

        energibridge_log.write(f'sampling interval: {sampling_interval}, target function: {target_function}, input size: {input_size}\n')
        energibridge_log.flush()
        energibridge_log.close()



    def interact(self, context: RunnerContext) -> None:
        """Perform any interaction with the running target system here, or block here until the target finishes."""
        # No interaction. We just run it for XX seconds.
        # Another example would be to wait for the target to finish, e.g. via `self.target.wait()`
        time.sleep(20)


    def stop_measurement(self, context: RunnerContext) -> None:
        """Perform any activity here required for stopping measurements."""
        # self.profiler.kill()
        self.profiler.wait()
        output.console_log("Energy measurement completed.")

    def stop_run(self, context: RunnerContext) -> None:
        """Perform any activity here required for stopping the run.
        Activities after stopping the run should also be performed here."""
        # self.target.kill()
        # self.target.wait()
        pass

    def populate_run_data(self, context: RunnerContext) -> Optional[Dict[str, Any]]:
        """Parse and process any measurement data here.
        You can also store the raw measurement data under `context.run_dir`
        Returns a dictionary with keys `self.run_table_model.data_columns` and their values populated"""

        remote_temporary_each_run_results_dir = f"{self.remote_temporary_results_dir}/{self.name}/run_{context.run_nr}"
        local_csv_path = context.run_dir / "energibridge.csv"
        local_log_path = context.run_dir / "energibridge.log"
        remote_csv_path = f"{remote_temporary_each_run_results_dir}/energibridge.csv"

        scp_csv_cmd = f"scp {self.remote_user}@{self.remote_host}:{remote_csv_path} {context.run_dir}"
        try:
            subprocess.run(shlex.split(scp_csv_cmd), check=True)
            output.console_log(
                f"Copied energibridge.csv rom remote directory to local directory: {context.run_dir}")
        except subprocess.CalledProcessError as e:
            output.console_log(f"Error during SCP: {e}")
            return None

        if not local_csv_path.exists():
            output.console_log(f"Error: File {local_csv_path} does not exist!")
            return None

        # energibridge.csv - Power consumption of the whole system
        df = pd.read_csv(local_csv_path)
        run_data = {
            'input_description': self.input_description[ math.ceil(context.run_nr/ (len(self.target_function_names) * len(self.sampling_rate_options))) - 1 ],
            'memory_usage': round(df.get('USED_MEMORY', pd.Series([0])).mean()/(1024 ** 2), 8),
            'dram_energy': round(df.get('DRAM_ENERGY (J)', pd.Series([0])).mean(), 8),
            'package_energy': round(df.get('PACKAGE_ENERGY (J)', pd.Series([0])).mean(), 8),
            'pp0_energy': round(df.get('PP0_ENERGY (J)', pd.Series([0])).mean(), 8),
            'pp1_energy': round(df.get('PP1_ENERGY (J)', pd.Series([0])).mean(), 8),
        }

        # Calculate average CPU usage across all cores
        cpu_columns = [col for col in df.columns if col.startswith('CPU_USAGE_')]
        if cpu_columns:
            core_avg_cpu_usage = df[cpu_columns].mean(axis=0)  # Sum up CPU usage of all cores for each row
            overall_avg_cpu_usage = core_avg_cpu_usage.mean()  # Compute the average CPU usage
            run_data['average_cpu_usage'] = round(overall_avg_cpu_usage, 8)

        if local_log_path.exists():
            try:
                # Implement retry mechanism to handle file read issues
                retries = 5  # Number of retries
                for attempt in range(retries):
                    try:
                        with open(local_log_path, 'r') as log_file:
                            log_content = log_file.read()
                            # Use regular expression to find the execution time in seconds
                            match = re.search(r"Energy consumption in joules: ([\d\.]+) for ([\d\.]+) sec of execution",
                                              log_content)
                            match_time1 = re.search(
                                r"first call execution time: ([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?) seconds", log_content)
                            match_time2 = re.search(
                                r"second call execution time: ([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?) seconds", log_content)
                            match_timetotal = re.search(
                                r"Total execution time: ([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?) seconds", log_content)
                            if match:
                                run_data['energy_consumption'] = float(
                                    match.group(1))  # Extract energy consumption in joules
                                run_data['execution_time'] = float(match_timetotal.group(1))
                                run_data['execution_time_1'] = float(
                                    match_time1.group(1))  # Extract the execution time in seconds
                                run_data['execution_time_2'] = float(
                                    match_time2.group(1))  # Extract the execution time in seconds
                            else:
                                output.console_log(
                                    f"Warning: No energy consumption or execution time found in {local_log_path}")
                                time.sleep(1)  # Wait for 1 second before retrying
                    except IOError:
                        output.console_log(f"Error reading file {local_log_path}. Retrying... ({attempt + 1}/{retries})")
                        time.sleep(1)  # Wait for 1 second before retrying

                if 'execution_time' and 'energy_consumption' not in run_data:
                    output.console_log(f"Error: Unable to retrieve execution time from {local_log_path} after {retries} attempts.")
            except Exception as e:
                output.console_log(f"Exception occurred while reading log file {local_log_path}: {e}")
        else:
            output.console_log(f"Error: Log file {local_log_path} does not exist.")
        return run_data

    def after_experiment(self) -> None:
        """Perform any activity required after stopping the experiment here
        Invoked only once during the lifetime of the program."""
        # run_table_path = self.results_output_path / self.name / 'run_table.csv'
        # processed_run_table_path = self.results_output_path / self.name / 'processed_run_table.csv'
        #
        # if not run_table_path.exists():
        #     output.console_log(f"Error: {run_table_path} does not exist.")
        #     return
        #
        # try:
        #     df = pd.read_csv(run_table_path)
        # except Exception as e:
        #     output.console_log(f"Error reading {run_table_path}: {e}")
        #     return
        #
        # if len(df) != 9:
        #     output.console_log(f"Error: {run_table_path} doesn't contain 9 rows.")
        #     return
        #
        # processed_df = df.copy()
        #
        # basic_average_cpu_usage = None
        # basic_memory_usage = None
        # basic_energy_consumption = None
        #
        # for index, row in df.iterrows():
        #     # calculate the row number, note that index starts from 1, except for the column name row
        #     row_num = index + 1
        #
        #     if row_num % 3 == 1:
        #         basic_average_cpu_usage = row['average_cpu_usage']
        #         basic_memory_usage = row['memory_usage']
        #         basic_energy_consumption = row['energy_consumption']
        #
        #         output.console_log(f"Row {row_num}: Basic strategy detected.")
        #         output.console_log(f"  Average CPU Usage: {basic_average_cpu_usage}")
        #         output.console_log(f"  Memory Usage: {basic_memory_usage}")
        #         output.console_log(f"  Energy Consumption: {basic_energy_consumption}")
        #
        #     else:
        #         if basic_average_cpu_usage is None:
        #             output.console_log(f"Error: Basic strategy values not set before row {row_num}.")
        #             return
        #
        #         current_average_cpu_usage = row['average_cpu_usage']
        #         current_memory_usage = row['memory_usage']
        #         current_energy_consumption = row['energy_consumption']
        #
        #         new_average_cpu_usage = current_average_cpu_usage - basic_average_cpu_usage
        #         new_memory_usage = current_memory_usage - basic_memory_usage
        #         new_energy_consumption = current_energy_consumption - basic_energy_consumption
        #
        #         processed_df.at[index, 'average_cpu_usage'] = new_average_cpu_usage
        #         processed_df.at[index, 'memory_usage'] = new_memory_usage
        #         processed_df.at[index, 'energy_consumption'] = new_energy_consumption
        #
        #         cache_strategy = 'cache' if row_num % 3 == 2 else 'lru_cache'
        #         output.console_log(f"Row {row_num}: {cache_strategy} strategy detected.")
        #         output.console_log(f"  Original Average CPU Usage: {current_average_cpu_usage}")
        #         output.console_log(f"  Original Memory Usage: {current_memory_usage}")
        #         output.console_log(f"  Original Energy Consumption: {current_energy_consumption}")
        #         output.console_log(f"  New Average CPU Usage: {new_average_cpu_usage}")
        #         output.console_log(f"  New Memory Usage: {new_memory_usage}")
        #         output.console_log(f"  New Energy Consumption: {new_energy_consumption}")
        #
        # try:
        #     processed_df.to_csv(processed_run_table_path, index=False)
        #     output.console_log(f"Processed run table saved to {processed_run_table_path}.")
        # except Exception as e:
        #     output.console_log(f"Error writing {processed_run_table_path}: {e}")
        return

    # ================================ DO NOT ALTER BELOW THIS LINE ================================
    experiment_path:            Path             = None
