from flask import Blueprint, request, render_template, g, session, redirect, url_for, jsonify

from flaskr.auth import login_required

# from flask_caching import Cache

from flaskr.miner import DataMiner

import os

# from bs4 import BeautifulSoup

import json

bp = Blueprint("webpage", __name__)

# # Configure Flask-Caching
# cache = Cache(config={'CACHE_TYPE': 'simple'})  # Use simple in-memory caching for demonstration purposes

@bp.route("/")
@login_required
def default_page():
    return render_template("base.html")


@bp.route("/home", methods = ("GET", "POST"))
@bp.route("/home/<boolean:new_request>", methods = ("GET", "POST"))
@login_required
def home(new_request = True):
    if new_request:
        if request.method == "POST":
            data = request.form
            website = data["website"]
            miner = DataMiner(website)

            #getting soup object
            soup = miner.fetch_and_parse()
            pretified_soup = miner.pretify_soup(soup)

            #saving the soup object in session
            bp.cache.set("soup", soup, timeout = 3600)

            #obtaining request response
            raw_source_json = miner.response_obj
            raw_source_json["soup"] = soup
            raw_source_json["pretified_soup"] = pretified_soup
            bp.cache.set("website", website, timeout = 3600)
            if raw_source_json:
                bp.cache.set("raw_source_json", raw_source_json, timeout = 3600)
            else:
                bp.cache.set("raw_source_json", None, timeout = 3600)
            return render_template("pages/home.html", raw_source_json = raw_source_json, website = website, header_list = None, mined_data = None)
        else:
            return render_template("pages/home.html", raw_source_json = None, website = None, header_list = None, mined_data = None)
    else:
        website = bp.cache.get("website")
        raw_source_json = bp.cache.get("raw_source_json")
        header_list = bp.cache.get("header_list")
        if not bp.cache.get("mined_data"):
            return render_template("pages/home.html", raw_source_json = None, website = None, header_list = None, mined_data = None)
        mined_data = json.loads(bp.cache.get("mined_data"))
        return render_template("pages/home.html", raw_source_json = raw_source_json, website = website, header_list = header_list, mined_data = mined_data)   

@bp.route("/iterative_data_miner", methods = ("GET", "POST"))
@login_required
def iterative_data_miner():
    data = {}
    if request.method == "POST":
        
        soup = bp.cache.get("soup")

        master_key = request.form.get("key")
        master_tag = request.form.get("tag") if request.form.get("tag") else None
        master_attribute = request.form.get("attribute") if request.form.get("attribute") else {}
        
        keys = request.form.getlist("key[]")
        tags = request.form.getlist("tag[]")
        attributes = request.form.getlist("attribute[]")

        # Saving the mining configuration
        config = {"config_type":"iterative"}
        config["key"] = master_key
        config["tag"] = master_tag
        config["attribute"] = master_attribute
        config["key[]"] = keys
        config["tag[]"] = tags
        config["attribute[]"] = attributes

        bp.cache.set("config", config, timeout = 3600)

        bp.cache.set("header_list", keys, timeout = 3600)

        element_list = DataMiner.find_elements(soup, master_tag, json.loads(master_attribute))

        if element_list:
            count = 0
            for element in element_list:
                element_data = {}
                for i in range(len(keys)):
                    tag = tags[i] if tags[i] else None
                    attribute = json.loads(attributes[i]) if attributes[i] else {}

                    if tag or attribute:
                        reqd_element = DataMiner.find_element(element, tag, attribute)
                    else:
                        reqd_element = element

                    if reqd_element:
                        text = DataMiner.extract_text(reqd_element)
                        url = DataMiner.extract_link(reqd_element)
                    else:
                        text = None
                        url = None
                    element_data[keys[i]] = {"text": text, "url": url}
                data[count] = element_data
                count += 1
        else:
            element_data = {}
            for i in range(len(keys)):
                element_data[keys[i]] = {"text": None, "url": None}
            data[0] = element_data

        bp.cache.set("mined_data", json.dumps(data), timeout = 3600)

        return redirect(url_for("webpage.home", new_request = False))

@bp.route("/procedural_data_miner", methods = ("GET", "POST"))
@login_required
def procedural_data_miner():
    data = {}
    if request.method == "POST":
        soup = bp.cache.get("soup")
        keys = request.form.getlist("key[]")
        tags = request.form.getlist("tag[]")
        attributes = request.form.getlist("attribute[]")

        # Saving the mining configuration
        config = {"config_type":"procedural"}
        config["key[]"] = keys
        config["tag[]"] = tags
        config["attribute[]"] = attributes

        bp.cache.set("config", config, timeout = 3600)

        bp.cache.set("header_list", keys, timeout = 3600)

        element_data = {}
        for i in range(len(keys)):
            tag = tags[i] if tags[i] else None
            attribute = json.loads(attributes[i]) if attributes[i] else {}
            if tag or attribute:
                reqd_element = DataMiner.find_element(soup, tag, attribute)
                if reqd_element:
                    text = DataMiner.extract_text(reqd_element)
                    url = DataMiner.extract_link(reqd_element)
                else:
                    text = None
                    url = None
                element_data[keys[i]] = {"text": text, "url": url}
            else:
                reqd_element = None
                element_data[keys[i]] = {"text": None, "url": None}
        data[0] = element_data

        bp.cache.set("mined_data", json.dumps(data), timeout = 3600)

        return redirect(url_for("webpage.home", new_request = False))
    
@bp.route("/saved_data_miner", methods = ["POST"])
@login_required
def saved_data_miner():
    config = request.json
    soup = bp.cache.get("soup")
    if not soup:
        return redirect(url_for("webpage.home"))
    if config["config_type"] == "iterative":
        data = {}
        master_key = config["key"]
        master_tag = config["tag"]
        master_attribute = config["attribute"]
        keys = config["key[]"]
        tags = config["tag[]"]
        attributes = config["attribute[]"]

        bp.cache.set("config", config, timeout = 3600)

        bp.cache.set("header_list", keys, timeout = 3600)

        element_list = DataMiner.find_elements(soup, master_tag, json.loads(master_attribute))

        if element_list:
            count = 0
            for element in element_list:
                element_data = {}
                for i in range(len(keys)):
                    tag = tags[i] if tags[i] else None
                    attribute = json.loads(attributes[i]) if attributes[i] else {}

                    if tag or attribute:
                        reqd_element = DataMiner.find_element(element, tag, attribute)
                    else:
                        reqd_element = element

                    if reqd_element:
                        text = DataMiner.extract_text(reqd_element)
                        url = DataMiner.extract_link(reqd_element)
                    else:
                        text = None
                        url = None
                    element_data[keys[i]] = {"text": text, "url": url}
                data[count] = element_data
                count += 1
        else:
            element_data = {}
            for i in range(len(keys)):
                element_data[keys[i]] = {"text": None, "url": None}
            data[0] = element_data

        mined_data = json.dumps(data)

        bp.cache.set("mined_data", mined_data, timeout = 3600)

        response = jsonify({"redirection_path": url_for("webpage.home", new_request = False)})

        response.status_code = 200

        return response
    else:
        data = {}

        keys = config["key[]"]
        tags = config["tag[]"]
        attributes = config["attribute[]"]

        bp.cache.set("config", config, timeout = 3600)

        bp.cache.set("header_list", keys, timeout = 3600)

        element_data = {}
        for i in range(len(keys)):
            tag = tags[i] if tags[i] else None
            attribute = json.loads(attributes[i]) if attributes[i] else {}
            if tag or attribute:
                reqd_element = DataMiner.find_element(soup, tag, attribute)
                if reqd_element:
                    text = DataMiner.extract_text(reqd_element)
                    url = DataMiner.extract_link(reqd_element)
                else:
                    text = None
                    url = None
                element_data[keys[i]] = {"text": text, "url": url}
            else:
                reqd_element = None
                element_data[keys[i]] = {"text": None, "url": None}
        data[0] = element_data

        mined_data = json.dumps(data)

        bp.cache.set("mined_data", mined_data, timeout = 3600)

        response = jsonify({"redirection_path": url_for("webpage.home", new_request = False)})

        response.status_code = 200

        return response

@bp.route("/save_config", methods = ["POST"])
@login_required
def save_config():
    config_name = request.form.get("configName")
    user_id = g.user["id"]
    error = None

    if not config_name:
        error = "Configuration name is required"
    else:
        config_file_name = config_name + ".json"

    if not error:
        user_folder_name = str(user_id)

        folder_path = os.path.join(os.getcwd(), "user_data", user_folder_name, 'config')

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print("Folder created successfully.")
        else:
            print("Folder already exists.")

        file_names = os.listdir(folder_path)

        if config_file_name in file_names:
            error = "A configuration already exists with this name"
            status_code = 500
        else:
            file_path = os.path.join(folder_path, config_file_name)
            try:
                config_json = bp.cache.get("config")
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(config_json, file)
                error = "Successfully saved configuration"
                status_code = 200
            except Exception as e:
                error = str(e)
                status_code = 500

    response_data = {"message":error, "message_id":"save-config-message"}

    response =  jsonify(response_data)

    response.status_code = status_code

    return response

@bp.route("/saved_config", methods = ["GET"])
@login_required
def saved_config():

    user_id = g.user["id"]

    user_folder_name = str(user_id)

    folder_path = os.path.join(os.getcwd(), "user_data", user_folder_name, 'config')

    if not os.path.exists(folder_path):
        config_files = []
    else:
        config_files = os.listdir(folder_path)

    response = jsonify({"config_files":config_files})

    response.status_code = 200

    return response

@bp.route("/load_config/<config_file>", methods = ["GET"])
@login_required
def load_config(config_file):

    user_id = g.user["id"]

    user_folder_name = str(user_id)

    folder_path = os.path.join(os.getcwd(), "user_data", user_folder_name, 'config')

    file_path = os.path.join(folder_path, config_file)

    with open(file_path, "r", encoding="utf-8") as file:
        config_json = json.load(file)

    response = jsonify({"config_json":config_json})

    response.status_code = 200

    # print(response)
    return response

@bp.route("/about")
@login_required
def about():
    return render_template("pages/about.html")
