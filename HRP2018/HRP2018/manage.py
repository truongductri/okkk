#!/usr/bin/env python
import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_PATH = os.path.dirname(os.path.realpath(__file__))

sys.path.append(REPO_PATH + os.sep + "apps")
sys.path.append(REPO_PATH + os.sep + "packages")
sys.path.append(REPO_PATH + os.sep + "packages/django")

extra_params = [x for x in sys.argv if x.count("--config=") > 0 ]

if __name__ == "__main__":
    

    # django.setup()

    if extra_params.__len__() == 0:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
        from django.core.management import execute_from_command_line
        import django
        execute_from_command_line(sys.argv)
    else:

        import imp
        settings = None
        config_file_param = [x for x in extra_params if x.split("=")[0] == "--config"]
        if config_file_param.__len__() > 0:
            file_name = config_file_param[0].split("=")[1]
            
            import imp
            settings = imp.new_module(file_name + ".settings")

            setattr(settings, "BASE_DIR", BASE_DIR)
            import json
            from exceptions import SyntaxError

            with open(os.path.dirname(__file__) + os.sep + "configs" + os.sep + file_name + '.json') as f:
                config_from_file = json.load(f)
                for x in config_from_file.get("PACKAGES", []):
                    sys.path.append(BASE_DIR + os.sep + x.replace("/", os.sep))
                    print("load path '{0}'".format(BASE_DIR + os.sep + x.replace("/", os.sep)))
                configs_items = []
                setattr(settings, "SECRET_KEY", config_from_file["SECRET_KEY"])
                for x in config_from_file.get("PACKAGES", []):
                    sys.path.append(BASE_DIR + os.sep + x.replace("/", os.sep))
                    print("add path'{0}'".format(BASE_DIR + os.sep + x.replace("/", os.sep)))
                for key in config_from_file.keys():
                    try:
                        if key == "LOGS":
                            pass
                        if key == "PACKAGES":
                            pass
                        elif key == "DB_BACK_END":
                            pass
                        elif key == "DB_API_CACHE":
                            pass
                        elif key == "AUTHORIZATION_ENGINE":
                            pass
                        elif key == "DB_AUTH":
                            import quicky

                            quicky.authorize.set_config(config_from_file[key])
                        elif key == "DB_LANGUAGE":
                            import quicky

                            quicky.language.set_config(config_from_file[key])
                        elif key == "DB_ENCRYPTOR_CACHE":
                            from quicky import encryptor

                            encryptor.set_config(config_from_file[key])
                        elif key == "DB_EXCEL_EXPORT_CONFIG":
                            from qexcel import language

                            language.set_config(config_from_file[key])
                        elif key == "DB_TRACKING":
                            import qtracking
                            qtracking.set_config(config_from_file[key])
                        elif key == "APPS":
                            pass
                        else:
                            setattr(settings, key, config_from_file[key])
                        configs_items.append(key)
                        print "load '{0}' with value {1}".format(key, config_from_file[key])
                    except SyntaxError as ex:
                        txt_loaded_items = ""
                        for x in configs_items:
                            txt_loaded_items = txt_loaded_items + "\n\t\t" + x
                        raise (Exception("load '{0}.json' error, see details:\nloaded items:\n{1}\n error at item:\n '{2}'\n error message:\n{3}".format(file_name, txt_loaded_items, key,ex.args.__str__())))
                    except Exception as ex:
                        txt_loaded_items = ""
                        for x in configs_items:
                            txt_loaded_items = txt_loaded_items + "\n\t\t" + x
                        raise (Exception("load '{0}.json' error, see details:\nloaded items:\n{1}\n error at item:\n '{2}'\n error message:\n{3}".format(file_name, txt_loaded_items, key, ex.message)))


            from django.conf.urls import url, include
            import quicky
            import importlib
            setattr(settings,"AUTHORIZATION_ENGINE",importlib.import_module(config_from_file["AUTHORIZATION_ENGINE"]))
            setattr(settings, "ROOT_URLCONF", 'apps')
            LOGGING = {
                'version': 1,
                'disable_existing_loggers': False,
                'handlers': {
                    'file': {
                        'level': 'DEBUG',
                        'class': 'logging.FileHandler',
                        'filename': BASE_DIR + os.sep+config_from_file.get("LOGS", 'logs' + os.sep + 'debug.log'),
                    },
                },
                'loggers': {
                    'django': {
                        'handlers': ['file'],
                        'level': 'DEBUG',
                        'propagate': False,
                    },
                },
            }
            setattr(settings, "LOGGING",LOGGING)
            #setattr(settings, "STATIC_URL", 'static/')
            #setattr(settings, "STATIC_ROOT",
            #        os.path.join(*(BASE_DIR.split(os.path.sep) + ['apps/static', 'apps/app_main/static'])))
            # sys.modules.update({file_name: {"settings": settings}})
            sys.modules.update({"settings": settings})
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
            from quicky import api
            api.connect(config_from_file["DB_API_CACHE"])
            from quicky import backends
            backends.set_config(config_from_file["DB_BACK_END"])
            quicky.url.build_urls(settings.ROOT_URLCONF,[x for x in config_from_file["APPS"] if not x.get("disable",False)] )
            from django.core.management import execute_from_command_line
            import django
            args = [x for x in sys.argv if x.count("--config=") == 0 ]
            execute_from_command_line(args)
