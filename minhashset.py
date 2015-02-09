import hashlib
import heapq

class MinhashSet(set):
    ''' Maintains a characteristic matrix of all the elements that are added
    into the set. Returns list of candidate duplicates'''


    def __init__(self):
        '''MinhashSet maintains an internal representation of the documents
        through a characteristic matrix. 

        The matrix is stored as a dictionary of
            { document_id : {set of up to 20 min hashes},
              document_id : {set of up to 20 min hashes} ... }

        If a document_id is not provided, the raw text is used as the key.
        
        Also a locality-sensitive hash is stored for each document_id. There
        are N buckets, and each document_id is labeled [0, N).

        '''

        self._char_matrix = {}
        self._lsh_buckets = {}
    
    def shingle(self, document, window_size=10):
        '''given a string, return the sliding window of characters'''
        shingles = set()
        for i in xrange(0, len(document)-window_size):
            shingles.add(document[i:i+window_size])

        return shingles
    
    def min_hashes(self, shingles):
        ''' Given an input list of shingles, return the 20 characteristic hashes.

        These are the 5 minimum hashes for each of 4 different hash functions.'''

        HASH_LEN = 64
        min_hash_heaps = {i: [] for i in range(4)}

        # generate twenty hash functions for shingles
        # want smallest hash result for each function
        for s in shingles:
            hasher = hashlib.sha256()
            hasher.update(s)
            hexdigest = hasher.hexdigest()

            # Each fourth of the SHA-256 digest is considered its own hash
            # Taken from http://okomestudio.net/biboroku/?p=2065
            for i in range(4):
                heapq.heappush(min_hash_heaps[i], hexdigest[i*HASH_LEN/4:(i+1)*HASH_LEN/4])


        # Final results are the 5 smallest hash results for each "function" (fourth)
        # Want total of 5 * 4 = 20 hashes.
            
        # Since we're using a set rather than a list, there is a chance that
        # the hashes will collide internally, causing less than 20 hashes to
        # fill the table. Given 64h/4 = 12 hex = 16**12 bit hashes, there is low chance
        # for a collision.

        min_hashes = set()
        for i in range(20):
            # The different hash function's outputs are interleaved in
            # the output. Nobody cares.
            try:
                min_hashes.add(heapq.heappop(min_hash_heaps[i%4]))
            except IndexError:
                # heapq throws IndexError when the heap is empty;
                # What to do when not enough data to generate 20 hash functions?
                
                # A fixed sentinel value will artificially inflate similarity
                # between tiny texts. That is fine, since the point is to lump similar
                # texts together to save computation time, and O(N^2) between tiny
                # documents is the cheapest.
                min_hashes.add('sentinel%d'%i)
        
        return min_hashes

    def add(self, document, document_id=None):
        '''Add a raw string document into the MinhashSet.
        
        Shingles as a preprocessing step'''
        
        if not isinstance(document, basestring):
            raise TypeError('MinhashSet.add can only process strings')
    
        # Use the raw document as a key if no ID is presented
        if not document_id: document_id = document
        
        # Collect sliding substring windows (aka shingles) of document
        shingles = self.shingle(document)

        # Collect 20 min hashes from the document. These form the document's
        # entry in the characteristic matrix.
        hashes = self.min_hashes(shingles)
        
        # Add hashes to a document's characteristic matrix
        self._char_matrix[document_id] = hashes
    
    def similarity_between(self, doc1, doc2):
        '''Computes the Jaccard similarity between two documents based off 
        their entries in the characteristic matrix.

        '''
        
        return len(self._char_matrix[doc1].intersection(self._char_matrix[doc2])) /\
                float(len(self._char_matrix[doc1].union(self._char_matrix[doc2])))
    
    
    def get_similar(self, docid, threshold=0.5):
        ''' Returns all documents similar enough to document indexed by docid
        with a Jaccard similarity score above the threshold'''
        
        results = []

        # TODO: use LSH to make this way more optimal
        # This should only iterate over documents in the same LSH bucket
        for doc in self._char_matrix:
            
            # Skip if it's the identity
            if doc == docid:
                continue

            # Calculate Jaccard similarity
            sim = self.similarity_between(docid, doc)
            
            # Add to results if it's high enough
            if sim >= threshold:
                results.append((sim, doc))

        return results
    
    def all_similar(self, threshold=0.5):
        ''' Returns clusters of documents that fall within a given threshold of one another,
        in the format {doc_id: [list of similar documents], 
                       doc_id: [list of similar documents],
                       ... }
        '''

        
        results = dict()

        # TODO: use LSH to make this way more optimal
        # This shouldn't be O(N^2).
        # Instead, only iterate within items that fall into the same LSH bucket
        for doc in self._char_matrix:
            results[doc] = self.get_similar(doc, threshold)
        
        return results

    def __repr__(self):
        '''Print raw characteristic matrix'''
        import pprint
        return pprint.pformat(self._char_matrix)

    def __str__(self):
        return self.__repr__()





