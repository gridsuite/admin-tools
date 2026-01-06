#
# Copyright (c) 2024, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests

import constant


#
# @author Kevin Le Saulnier <kevin.lesaulnier at rte-france.com>
#

def get_folders():
    result_content = ''
    try:
        result = requests.get(constant.GRAFANA_FOLDER_URL, {'parentUid' : 'e6eb2338-0ab9-45e4-ba3b-8df649ddd4c3'})
        result_content = result.json()
        # grafana errors are details in request content
        result.raise_for_status()
        return result_content
    except Exception as e:
        raise SystemExit(e, result_content)

def create_folder(folder_name, parent_folder_uid = ''):
    return __create_folder({'title': folder_name, 'parentUid' : parent_folder_uid})

def __create_folder(json_data):
    result_content = ''
    try:
        print("Create folder : %s - %s" % (json_data['title'], json_data['parentUid']))
        result = requests.post(constant.GRAFANA_FOLDER_URL, json=json_data, headers=constant.GRAFANA_HEADERS, cookies=constant.GRAFANA_COOKIES)
        result_content = result.content
        result.raise_for_status()
        print("Folder successfully (re)created : %s" % json_data['title'])
        return result.json()['uid']
    except Exception as e:
        if result.status_code == requests.codes.conflict:
            print("Folder already exist : %s" % json_data['title'])
        else:
            raise SystemExit(e, result_content)

def get_folder(folder_uuid):
    result_content = ''
    try:
        result = requests.get(get_folder_url(folder_uuid), headers=constant.GRAFANA_HEADERS, cookies=constant.GRAFANA_COOKIES)
        result_content = result.content
        result.raise_for_status()
        return result.json()
    except Exception as e:
        raise SystemExit(e, result_content)

def delete_folder(folder_uuid):
    result_content = ''
    try:
        result = requests.delete(get_folder_url(folder_uuid), headers=constant.GRAFANA_HEADERS, cookies=constant.GRAFANA_COOKIES)
        result_content = result.content
        result.raise_for_status()
        print("Folder successfully deleted : %s" % folder_uuid)
    except Exception as e:
        raise SystemExit(e, result_content)

def reset_folder(folder_uuid):
    folder_json = get_folder(folder_uuid)
    delete_folder(folder_uuid)
    __create_folder(folder_json)

def get_folder_url(folder_uuid):
    return constant.GRAFANA_FOLDER_URL + '/' + folder_uuid