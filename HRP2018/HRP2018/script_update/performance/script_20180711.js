var $$schema = 'lv';
var $$separate = '.';

db.system.js.deleteOne({ "_id": "getListPermission" });
db.system.js.save(
    {
        _id: "getListPermission",
        value: function (schema, appName, roleCode) {
            var permissions = db.getCollection(schema + "." + 'AD_Roles').aggregate([
                { $unwind: { path: "$permission", preserveNullAndEmptyArrays: false } },
                {
                    $project: {
                        "_id": 0,
                        "role_code": "$role_code",
                        "function_id": "$permission.function_id",
                        "read": "$permission.read",
                        "create": "$permission.create",
                        "write": "$permission.write",
                        "delete": "$permission.delete",
                        "export": "$permission.export",
                        "import": "$permission.import",
                        "copy": "$permission.copy",
                        "attach": "$permission.attach",
                        "download": "$permission.download",
                        "created_by": "$permission.created_by",
                        "created_on": "$permission.created_on",
                        "modified_by": "$permission.modified_by",
                        "modified_on": "$permission.modified_on"
                    }
                },
                { "$match": { "role_code": roleCode } }
            ]).toArray();
            var list_function_id = [];
            var rs = [];
            permissions.forEach(function (e) {
                list_function_id.push(e.function_id);
                var rec = db.getCollection(schema + "." + 'SYS_FunctionList').find({ $and: [{ "app": appName }, { "function_id": e.function_id }] })[0];
                if (rec) {
                    rec['level_code'].forEach(
                        function (el) {
                            var fil = list_function_id.filter(function (val) { return val == el; });
                            if (fil.length === 0)
                                list_function_id.push(el);
                        })
                }
            })
            var fnc_list = db.getCollection(schema + "." + 'SYS_FunctionList').find({ "function_id": { "$in": list_function_id } });
            fnc_list.forEach(function (e) {
                var filter = permissions.filter(x => x.function_id === e.function_id);
                if (filter.length === 0) {
                    rs.push({
                        'function_id': e.function_id,
                        'default_name': e.default_name,
                        'parent_id': e.parent_id,
                        'role_code': roleCode,
                        'copy': false,
                        'read': false,
                        'create': false,
                        'created_by': null,
                        'write': false,
                        'attach': false,
                        'created_on': false,
                        'export': false,
                        'download': false,
                        'import': false,
                        'delete': false
                    });
                } else {
                    var value = filter[0];
                    rs.push({
                        'function_id': value.function_id,
                        'default_name': e.default_name,
                        'parent_id': e.parent_id,
                        'role_code': roleCode,
                        'copy': value.copy,
                        'read': value.read,
                        'create': value.create,
                        'created_by': value.created_by,
                        'write': value.write,
                        'attach': value.attach,
                        'created_on': value.created_on,
                        'export': value.export,
                        'download': value.download,
                        'import': value.import,
                        'delete': value.delete
                    });
                }
            });

            return rs;
        }
    }
);

db.system.js.deleteOne({ "_id": "getEmployeeByDepartmentCode" });
db.system.js.save(
    {
        _id: "getEmployeeByDepartmentCode",
        value: function (schema, appName, departmentCode, pageSize, pageIndex, sort, search) {
            var departments = db.getCollection(schema + "." + 'HCSSYS_Departments').aggregate([
                { $match: { 'level_code': departmentCode } },
                { $project: { 'department_code': 1, 'level_code': 1, 'level': 1 } }
            ]).toArray();

            var rs = [];
            var lstDepartmentCode = [];
            departments.forEach(function (el) {
                lstDepartmentCode = lstDepartmentCode.concat(el.level_code.slice(el.level_code.indexOf(departmentCode), el.level_code.length));
            });

            rs = db.getCollection(schema + "." + 'SYS_ValueList').aggregate([
                { $match: { list_name: "LGender" } },
                { $unwind: { path: "$values", preserveNullAndEmptyArrays: false } },
                { $lookup: { from: schema + "." + "HCSEM_Employees", localField: "values.value", foreignField: "gender", as: "emp" } },
                { $unwind: { path: "$emp", preserveNullAndEmptyArrays: true } },
                { $lookup: { from: schema + "." + "HCSSYS_Departments", localField: "emp.department_code", foreignField: "department_code", as: "dept" } },
                { $unwind: { path: "$dept", preserveNullAndEmptyArrays: false } },
                {
                    $project: {
                        "full_name": { $concat: ["$emp.last_name", " ", "$emp.first_name"] },
                        "employee_code": "$emp.employee_code",
                        "gender": "$values.caption",
                        "job_w_code": "$emp.job_w_code",
                        "join_date": "$emp.join_date",
                        "department_code": "$emp.department_code",
                        "department_name": "$dept.department_name",
                        "photo_id": "$emp.photo_id",
                        "last_name": "$emp.last_name",
                        "first_name": "$emp.first_name",
                        "extra_name": "$emp.extra_name",
                        "birthday": "$emp.birthday",
                        "b_province_code": "$emp.b_province_code",
                        "nation_code": "$emp.nation_code",
                        "ethnic_code": "$emp.ethnic_code",
                        "religion_code": "$emp.religion_code",
                        "culture_id": "$emp.culture_id",
                        "is_retrain": "$emp.is_retrain",
                        "train_level_code": "$emp.train_level_code",
                        "marital_code": "$emp.marital_code",
                        "id_card_no": "$emp.id_card_no",
                        "issued_date": "$emp.issued_date",
                        "issued_place_code": "$emp.issued_place_code",
                        "mobile": "$emp.mobile",
                        "p_phone": "$emp.p_phone",
                        "email": "$emp.email",
                        "personal_email": "$emp.personal_email",
                        "document_no": "$emp.document_no",
                        "official_date": "$emp.official_date",
                        "career_date": "$emp.career_date",
                        "personnel_date": "$emp.personnel_date",
                        "emp_type_code": "$emp.emp_type_code",
                        "labour_type": "$emp.labour_type",
                        "job_pos_code": "$emp.job_pos_code",
                        "job_pos_date": "$emp.job_pos_date",
                        "job_w_date": "$emp.job_w_date",
                        "profession_code": "$emp.profession_code",
                        "level_management": "$emp.level_management",
                        "is_cbcc": "$emp.is_cbcc",
                        "is_expert_recruit": "$emp.is_expert_recruit",
                        "is_expert_train": "$emp.is_expert_train",
                        "manager_code": "$emp.manager_code",
                        "manager_sub_code": "$emp.manager_sub_code",
                        "user_id": "$emp.user_id",
                        "job_pos_hold_code": "$emp.job_pos_hold_code",
                        "job_w_hold_code": "$emp.job_w_hold_code",
                        "department_code_hold": "$emp.department_code_hold",
                        "job_pos_hold_from_date": "$emp.job_pos_hold_from_date",
                        "job_pos_hold_to_date": "$emp.job_pos_hold_to_date",
                        "end_date": "$emp.end_date",
                        "retire_ref_no": "$emp.retire_ref_no",
                        "signed_date": "$emp.signed_date",
                        "signed_person": "$emp.signed_person",
                        "active": "$emp.active",
                        "note": "$emp.note",
                        "p_address": "$emp.p_address",
                        "p_province_code": "$emp.p_province_code",
                        "p_district_code": "$emp.p_district_code",
                        "p_ward_code": "$emp.p_ward_code",
                        "p_hamlet_code": "$emp.p_hamlet_code",
                        "t_address": "$emp.t_address",
                        "t_province_code": "$emp.t_province_code",
                        "t_district_code": "$emp.t_district_code",
                        "t_ward_code": "$emp.t_ward_code",
                        "t_hamlet_code": "$emp.t_hamlet_code",
                        "foreigner": "$emp.foreigner",
                        "vn_foreigner": "$emp.vn_foreigner",
                        "is_not_reside": "$emp.is_not_reside",
                        "fo_working": "$emp.fo_working",
                        "fo_permiss": "$emp.fo_permiss",
                        "fo_begin_date": "$emp.fo_begin_date",
                        "fo_end_date": "$emp.fo_end_date"
                    }
                },
                { $match: { "department_code": { $in: lstDepartmentCode } } },
                {
                    $match: {
                        $or: [
                            { "full_name": { $regex: search, $options: 'i' } },
                            { "employee_code": { $regex: search, $options: 'i' } },
                            { "gender": { $regex: search, $options: 'i' } },
                            { "job_w_code": { $regex: search, $options: 'i' } },
                            { "join_date": { $regex: search, $options: 'i' } },
                            { "department_name": { $regex: search, $options: 'i' } }
                        ]
                    }
                },
                { $sort: sort },
                {
                    $facet: {
                        metadata: [{ $count: "total" }, { $addFields: { page_index: pageIndex, page_size: pageSize } }],
                        data: [{ $skip: pageSize * pageIndex }, { $limit: pageSize }]
                    }
                },
                { $unwind: { path: '$metadata', preserveNullAndEmptyArrays: false } },
                {
                    $project: {
                        'page_size': '$metadata.page_size',
                        'page_index': '$metadata.page_index',
                        'total_items': '$metadata.total',
                        'items': '$data',
                    }
                }
            ]).toArray();

            if (rs.length > 0) {
                return rs[0];
            }
            return {
                'page_size': pageSize,
                'page_index': pageIndex,
                'total_items': 0,
                'items': [],
            };
        }
    }
);

//Create collection TMSYS_ConfigChangeObjectPriority và init data
db.createCollection($$schema + $$separate + 'TMSYS_ConfigChangeObjectPriority');
db.getCollection($$schema + $$separate + 'TMSYS_ConfigChangeObjectPriority').insert(
    [
        {
            "value_list_key": "TMChangeObjectRank",
            "change_object": 1,
            "name": "Nhóm Chức danh công việc",
            "priority_no": 1,
            "note": "Đối tượng thiết lập Xếp loại cá nhân",
            "language": "vn",
            "created_on": new Date,
            "created_by": "application",
            "modified_on": null,
            "modified_by": null
        },
        {
            "value_list_key": "TMChangeObjectRank",
            "change_object": 2,
            "name": "Chức danh công việc",
            "priority_no": 2,
            "note": "Đối tượng thiết lập Xếp loại cá nhân",
            "language": "vn",
            "created_on": new Date,
            "created_by": "application",
            "modified_on": null,
            "modified_by": null
        },
        {
            "value_list_key": "TMChangeObjectRank",
            "change_object": 3,
            "name": "Chức vụ",
            "priority_no": 3,
            "note": "Đối tượng thiết lập Xếp loại cá nhân",
            "language": "vn",
            "created_on": new Date,
            "created_by": "application",
            "modified_on": null,
            "modified_by": null
        },
        {
            "value_list_key": "TMChangeObjectRank",
            "change_object": 4,
            "name": "Loại nhân viên",
            "priority_no": 4,
            "note": "Đối tượng thiết lập Xếp loại cá nhân",
            "language": "vn",
            "created_on": new Date,
            "created_by": "application",
            "modified_on": null,
            "modified_by": null
        }
    ]
);