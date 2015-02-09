from minhashset import MinhashSet
import nose
from nose.tools import *

lorem_ipsum_1 = '''Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"
            '''

# Different than lorem_ipsum_1 only by the last character
lorem_ipsum_2 = '''Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur."
            '''

# Half of lorem_ipsum_1
lorem_ipsum_1_short = '''Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.'''

def test_initialize():
    mhs = MinhashSet()
    eq_(len(mhs._char_matrix), 0)

def test_add_one_lengths():
    '''Basic test to make sure lengths of data structures match up'''

    mhs = MinhashSet()
    mhs.add(lorem_ipsum_1, 'document_1')

    eq_(len(mhs._char_matrix), 1)
    eq_(len(mhs._char_matrix['document_1']), 20)

def test_identities():
    mhs = MinhashSet()
    mhs.add(lorem_ipsum_1, 'document_1')
    mhs.add(lorem_ipsum_1, 'document_2')
    mhs.add('', 'empty')

    eq_(mhs.similarity_between('document_1', 'document_2'), 1)
    eq_(mhs.similarity_between('document_1', 'empty'), 0)
    eq_(mhs.similarity_between('empty', 'empty'), 1)

def test_get_similar():
    mhs = MinhashSet()
    mhs.add(lorem_ipsum_1, 'doc1')
    mhs.add(lorem_ipsum_2, 'doc2')

    # There are no guarantees about lorem_ipsum_1_short, because the min hashes
    # could take place in the removed section or in the existing section

    # However, doc2 is guaranteed to have at maximum one difference in their minhash
    eq_(mhs.get_similar('doc1', threshold=0.95)[0][1], 'doc2')

    # This is useless, because we can't test that doc1 and doc2 are NOT 1, because
    # there is no guarantee unless we calculate the hashes out ahead of time.

    # That might be worth doing in this case.

