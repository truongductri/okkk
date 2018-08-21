How to create view with qmongo:
-------------------------------

1. Create from aggregate of model:

    Example:

        .. code-block::

            from qmongo import qview
            from qmongo import database
            from qmongo import helpers
            db = database.connect( host="localhost",port=27017,name="mydb",user="myusername",password="mypassword")
            helpers.define_model(
                            "my_model",
                [["code"],["email"]],
                dict(
                    _id=helpers.create_field("text"),
                    code = helpers.create_field("text",True),
                    first_name = helpers.create_field("text",True),
                    last_name = helpers.create_field("text",True),
                    email = helpers.create_field("text",True),
                    created_on=helpers.create_field("date",True),
                    created_by=helpers.create_field("text",True),
                    modified_on=helpers.create_field("date"),
                    modified_by=helpers.create_field("text")
                )
            )
            coll = db.collection("my_model")
            qr=coll.aggregate().project(
                code=1,
                full_name="first_name+' '+last_name",
                email=1)
            my_view=qview.create_mongodb_view(qr,"my_view")
            items = list(my_view)
2. Create from pipeline aggregate builder:

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
           from qmongo import qview

           from pymongo import MongoClient
           cnn =  MongoClient(host="localhost",port=27017)
           db = cnn.get_database("mydb")


           my_view_name=qview.create_mongod_view_from_pipeline(
                                db,
                                mongo_expr.get_pipe(),
                                "my_collection",
                                "myschema",
                                "my_view"
           )
           items=list(db.get_collection(my_view_name).find())
           print items






