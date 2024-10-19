#AI generated for explorative purposes

<<<<<<< HEAD
from functools import cache, lru_cache
#from pyJoules.device.rapl_device import RaplPackageDomain
#from pyJoules.energy_meter import measure_energy
import spacy
=======
from functools import cache, lru_cache, wraps
import spacy
from time import perf_counter

def timer(func, *args, **kwargs):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        print(f'Starting {func.__name__} at {start}')   # 1
        result = func(*args, **kwargs)
        end = perf_counter()
        print(f'Finished {func.__name__} at {end}')     # 3
        print(f"Elapsed time: {end - start}")           # 4
        return result                                   # 5                
    return wrapper

@timer
def measure_time(func: callable, *args, **kwargs):
    print(f"Calling {func.__name__} with args: {args}")  # 2
    return func(*args, **kwargs)
>>>>>>> 82983cb (code running on raspberry PI 4)

nlp = spacy.load("en_core_web_sm")

# Basic Implementation
<<<<<<< HEAD
#@measure_energy(domains=[RaplPackageDomain(0)])
=======
>>>>>>> 82983cb (code running on raspberry PI 4)
def lemmatization(nlp: spacy.language.Language, sentence: str) -> str:
    doc = nlp(sentence)
    lemmatized_sentence = ' '.join([token.lemma_ for token in doc])
    return lemmatized_sentence

# Using functools.cache (Python 3.9+)
<<<<<<< HEAD
#@measure_energy(domains=[RaplPackageDomain(0)])
=======
>>>>>>> 82983cb (code running on raspberry PI 4)
@cache
def lemmatization_cache(nlp: spacy.language.Language, sentence: str) -> str:    
    doc = nlp(sentence)
    lemmatized_sentence = ' '.join([token.lemma_ for token in doc])
    return lemmatized_sentence

# Using functools.lru_cache
<<<<<<< HEAD
#@measure_energy(domains=[RaplPackageDomain(0)])
=======
>>>>>>> 82983cb (code running on raspberry PI 4)
@lru_cache(maxsize=None)
def lemmatization_lru_cache(nlp: spacy.language.Language, sentence: str) -> str:
    doc = nlp(sentence)
    lemmatized_sentence = ' '.join([token.lemma_ for token in doc])
    return lemmatized_sentence

if __name__ == '__main__':
    # Example usage
    sentence = "The quick brown foxes are jumping over the lazy dogs"

    print(lemmatization(nlp, sentence))
<<<<<<< HEAD
    print(lemmatization_cache(nlp, sentence))
    print(lemmatization_lru_cache(nlp, sentence))













"""
@measure_energy(domains=[RaplPackageDomain(0)])
def mandelbrot():
    w = h = x = y = bit_num = 0
    byte_acc = 0
    i = 0; iterations = 50
    limit = 2.0
    Zr = Zi = Cr = Ci = Tr = Ti = 0.0

    w = int(sys.argv[1])
    h = w

    sys.stdout.write(f'P4\n{w} {h}\n'); sys.stdout.flush()

    for y in range(h):

        for x in range(w):

            Zr = Zi = 0.0 
            Cr = (2.0 * x / w - 1.5); Ci = (2.0 * y / h - 1.0)        
        
            for i in range(iterations):

                Tr = Zr*Zr - Zi*Zi + Cr
                Ti = 2*Zr*Zi + Ci          
                Zr = Tr; Zi = Ti               
                if Zr*Zr+Zi*Zi > limit*limit:
                    break
            
            
            if Zr*Zr+Zi*Zi > limit*limit: 
                byte_acc = (byte_acc << 1) | 0x00
            else:
                byte_acc = (byte_acc << 1) | 0x01
                
            bit_num += 1         

            if bit_num == 8:
                # Python 2.7 sys.stdout.write(chr(byte_acc))
                sys.stdout.buffer.write(bytes([byte_acc]))        
                byte_acc = 0
                bit_num = 0

            elif x == w - 1:

                byte_acc = byte_acc << (8-w%8)   
                sys.stdout.buffer.write(bytes([byte_acc]))  
                byte_acc = 0
                bit_num = 0
"""
=======
    print(measure_time(lemmatization, nlp, sentence))
    
    print(measure_time(lemmatization_cache, nlp, sentence))
    print(measure_time(lemmatization_cache, nlp, sentence))

    print(measure_time(lemmatization_lru_cache, nlp, sentence))
    print(measure_time(lemmatization_lru_cache, nlp, sentence))

    assert lemmatization(nlp, sentence) == lemmatization_cache(nlp, sentence) == lemmatization_lru_cache(nlp, sentence)
>>>>>>> 82983cb (code running on raspberry PI 4)
