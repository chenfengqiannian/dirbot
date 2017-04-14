from scrapy.exceptions import DropItem
import MySQLdb
import logging
import re
logger = logging.getLogger(__name__)
class WriteDatabasePipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""

    # put all words in lowercase
    words_to_filter = ['politics', 'religion']
    def open_spider(self,spider):
        self.conn= MySQLdb.connect(db='zhaogefang', host='127.0.0.1', user='zhaogefang', passwd='ZgFqweasd123',charset="utf8")

        logger.debug("start connect##################")


        return
    def close_spider(self,spider):
        self.conn.close()
        logger.debug("close connect##################")
        return
    def process_item(self, item, spider):

        cursor = self.conn.cursor()

        if("tel" not in item or item['tel']==""):
            raise DropItem("no tel")
        item["tel"]=item["tel"].replace(' ', '').replace("tel:","")

        cursor = self.conn.cursor()
        b=re.compile("(\d{4})")
        a=re.compile("(\d{11})")
	if("builddate" in item):
	    if(b.match(item["builddate"])==None):
		#print ("MMMMMMMMMMMMMMMMMMMMMM")
		item["builddate"]=0
        if(a.match(item["tel"])==None):
            raise DropItem("no tel")
        if("community" in item):
            sql = "SELECT * FROM %s_house_leasesale_gather WHERE tel = '%s' AND community = '%s'" % (item['cityjx'],item['tel'],item["community"])

            cursor.execute(sql)
            if(cursor.rowcount>=1):
                raise DropItem("exist item")

        for i in item.keys():
            if type(item[i])==list:
                item[i]=''.join(item[i])


        keys=item.keys()
        value=item.values()
        keys = keys.__str__()
        value=value.__str__()
        keys = keys.replace("[", "(")
        keys = keys.replace("]", ")")
        keys = keys.replace("'", "")
        value = value.replace("[", "(")
        value = value.replace("]", ")")
        value = value.replace(" ", "")
        value = value.replace("\n", "")
        value = value.replace("\r", "")
        value = value.replace("u'", "'")
        value=value.decode('unicode_escape')
        #print "#####################"

        sqlinsert = "INSERT INTO jn_house_leasesale_gather "+keys+" VALUES "+value

        #print sqlinsert
        try:

            cursor.execute(sqlinsert)

            self.conn.commit()
            #print u"success"
        except Exception, e:
            print e
		# Rollback in case there is any error
            #print u"fial"
            self.conn.rollback()






        return item

