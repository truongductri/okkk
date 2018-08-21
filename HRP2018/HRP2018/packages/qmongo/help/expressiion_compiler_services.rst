qmongo supports 2 usefull services for transfering natural expression into tree expression of Mongodb are inlcudes:

1- filter_expression
2- aggregate_expression

filter_expression
===================

**filter_expression**: Use for find,find one, update, update one or in match pipeline aggregate framework.


    Example:

    .. code-block::

        from qmongo import helpers
        f_with_constants = helpers.filter("a>1 and b<2")
        f_with_params = helpers.filter("a{0}1 and a<{1}",50,1000)
        import pymongo
        cnn = pymongo.mongo_client.MongoClient(host="localhost",port=27017)
        db = cnn.get_database("my_test")
        my_collection = db.get_collection("my_collection")

        my_collection.find_one(f_with_constants.get_filter())

        my_collection.find_one(f_with_params.get_filter())

        list(my_collection.aggregate([{"$match":f_with_constants.get_filter()}]))

        list(my_collection.aggregate([{"$match":f_with_params.get_filter()}]))

    filter_expression is also support text function such as: contains, start,end:

        Example:

            .. code-block::

                from qmongo import helpers
                find_start_with = helpers.filter("start(a,'xxx')")
                find_start_with_param = helpers.filter("start(a,{0})","12345")





aggregate_expression
--------------------

**aggregate_expression**: Use to make a chains of aggregate item in a pipeline aggregation framework



    Example:

    .. code-block::

       from qmongo import helpers
       mongo_expr = helpers.aggregate_expression().match("year > 2005 and year<=2011")

       mongo_expr = helpers.aggregate_expression().match("year > {0} and year<={1}",2005,2011)
       mongo_expr.sort(year=-1)
       mongo_expr.sort({"year":-1})
       mongo_expr.sort({"year":-1})
       mongo_expr.select({"a":"b+{0}","c":1,"d":1},2000)
       mongo_expr.select(a="b+2000")
       print mongo_expr.get_pipe()


