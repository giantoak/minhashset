import sqlalchemy
from sqlalchemy import text
import sys
import os
from bs4 import BeautifulSoup as bs

texas = """abilene
amarillo
austin
beaumont
brownsville
collegestation
corpuschristi
dallas
delrio
denton
elpaso
fortworth
galveston
houston
huntsville
killeen
laredo
lubbock
mcallen
midcities
odessa
sanantonio
sanmarcos
texarkana
texomaland
tyler
victoria
waco
wichitafalls"""

locs = texas.split('\n')

engine = sqlalchemy.create_engine('mysql+pymysql://acorn:acornacornacorn@acornht.cfalas7jic14.us-east-1.rds.amazonaws.com/memex_ht')
conn = engine.connect()

def get_shingles(a, window_size=10):
    '''given a string, return the sliding window of characters'''
    shingles = {}
    for i in xrange(0, len(a)-window_size):
        shingles.add(a[i:i+window_size])

    return shingles

def min_hash(shingles):
    ''' Given an input set A, compute the hash across a variety of different hash functions
    
    for N hashes, return an AxN array of hash results'''

    HASH_LEN = 64
    min_hash_heaps = {i: [] for i in range(4)}
    
    # generate twenty hash functions for shingles
    # want smallest hash result for each function
    for s in shingles:
        hasher = hashlib.sha256()
        hasher.update(s)
        hexdigest = hasher.hex_digest()
        
        # Each fourth of the SHA-256 digest is considered its own hash
        # Taken from http://okomestudio.net/biboroku/?p=2065
        for i in range(4):
            heapq.heappush(hexdigest[i*HASH_LEN/4:(i+1)*HASH_LEN/4], min_hash_heaps[i])
    
    
    # Final results are the 5 smallest hash results for each "function" (fourth)
    # Want total of 5 * 4 = 20 hashes.

    min_hashes = []
    for i in range(20):
        min_hashes.append(heapq.heappop(min_hash_heaps[i%4]))

    return min_hashes



def near_similar(a, b):
    shingles = get_shingles(a)
    min_hashes = min_hash(shingles)

    shingles_b = get_shingles(b)
    min_hashes_b = min_hash(shingles_b)

    return len(min_hashes.intersection(min_hashes_b))  \
        / len(min_hashes.union(min_hashes_b)) > JACCARD_THRESHOLD

with open('bp_tx.csv', 'r') as infile:
    for line in infile:
        url, place, jobtype, number, postdate = line.split('\t')
        r = conn.execute(text('SELECT id, body FROM backpage_incoming WHERE url = :qstr'), qstr=url)
        for doc_id, ad in r:
            min_hash_set.add(ad, doc_id)

        for a1, a2 in min_hash_set.all_near_similar():
            #extract phone numbers from either ad
            phone1 = extract_phone(a1)
            phone2 = extract_phone(a2)
            save(a1, a2, phone1, phone2, matches)

        s = bs(str(ad))
        body = s.select('#pageBackground > div.mainBody > div.posting > div.postingBody')[0]\
            .getText().decode('string_escape').strip(' \r\n\t')
        print body
        pass

