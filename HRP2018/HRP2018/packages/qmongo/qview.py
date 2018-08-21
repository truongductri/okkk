_cach_view={}
from database import AGGREGATE
import helpers
def create_mongodb_view(aggregate,name):
    if not isinstance(aggregate,AGGREGATE):
        raise (Exception("It looks like you create view from object is not '{0}'".format("qmomgo.database.AGGREGATE")))
    global _cach_view
    import json
    view_name = "{0}.{1}".format(aggregate._coll.schema, name)
    command_object = (
        view_name,
        aggregate._coll.get_collection_name(),
        aggregate._pipe
    )
    if not _cach_view.has_key(view_name):
        aggregate._coll.qr.db.drop_collection(view_name)
        param_text = json.dumps(command_object)
        param_text = param_text[1:param_text.__len__() - 1]
        command_text = "db.createView(" + param_text + ")"
        aggregate._coll.qr.db.eval(command_text)
        _cach_view[view_name] = 1
        view_model_fields={}
        for field in aggregate.get_selected_fields():
            view_model_fields.update(
                {field:helpers.create_field("text", False)}
            )

        helpers.define_model(
            name,
            [],
            view_model_fields
        )
    ret=aggregate.qr.collection(name)
    return ret
def create_mongod_view_from_pipeline(db,pipe_line,from_collection,schema,view_name):

    global _cach_view
    import json
    view_name = "{0}.views.{1}".format(schema, view_name)
    command_object = (
        view_name,
        "{0}.{1}".format(schema,from_collection),
        pipe_line
    )
    if not _cach_view.has_key(view_name):
        db.drop_collection(view_name)
        param_text = json.dumps(command_object)
        param_text = param_text[1:param_text.__len__() - 1]
        command_text = "db.createView(" + param_text + ")"
        db.eval(command_text)
        _cach_view[view_name] = 1
        view_model_fields={}
    return view_name
