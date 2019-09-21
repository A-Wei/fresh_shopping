from haystack import indexes
from goods.models import GoodsSKU

class GoodsSKUIndex(indexes.SearchIndex, indexes.Indexable):
    #索引字段 use_template=True 指定根据表中的那些字段建立索引文件，把说明放在一个文件中。
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return GoodsSKU

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
