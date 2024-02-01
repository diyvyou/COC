from flask import Flask,render_template,request
import json
import os
import random

app = Flask(__name__)

@app.route("/")
def main():
    characters = get_saved_characters()
    return render_template("list.html",characters=characters)

@app.route("/handle_button", methods=["POST"])
def button_chick():
    global constitution_value,will_value,aglie_value,strength_value,inspiration_value,HPs,SANs
    constitution_value = num_random(3,6) * 5
    will_value = num_random(3,6) * 5
    aglie_value = num_random(3,6) * 5
    strength_value = num_random(3,6) * 5
    inspiration_value = num_random(3,6) * 5
    HPs = (constitution_value + 65)/10
    SANs = will_value
    return render_template("indexs.html",constitution_value=constitution_value,will_value=will_value,aglie_value=aglie_value,strength_value=strength_value,inspiration_value=inspiration_value,HP=HPs,SAN=SANs)

@app.route("/save_to_json", methods=["POST"])
def save_to_json():
    char_name = request.form.get("charName")

    data_to_save = {
        "char_name": char_name,
        "constitution_value": constitution_value,
        "will_value": will_value,
        "aglie_value": aglie_value,
        "strength_value": strength_value,
        "inspiration_value": inspiration_value,
        "HP": HPs,
        "SAN": SANs,
    }

    # 使用角色名作为JSON文件名，并确保支持中文字符
    json_filename = f"file/{char_name}.json"
    with open(json_filename, "w", encoding="utf-8") as json_file:
        json.dump(data_to_save, json_file, ensure_ascii=False)

    return "数据成功保存到JSON文件中！"


# 查看角色详细数据视图
@app.route("/view_character/<char_name>")
def view_character(char_name):
    json_filename = f"file/{char_name}.json"
    character_data = load_character_data(json_filename)
    return render_template("character_details.html", char_name=char_name, character_data=character_data)

# 辅助函数：获取所有保存的角色名
def get_saved_characters():
    characters = []
    for filename in os.listdir("file"):
        if filename.endswith(".json"):
            # 从文件名中提取角色名
            char_name = os.path.splitext(filename)[0]
            characters.append(char_name)
    return characters

# 辅助函数：从JSON文件中加载角色详细数据
def load_character_data(json_filename):
    with open(json_filename, "r", encoding="utf-8") as json_file:
        character_data = json.load(json_file)
        #print (character_data.HP)
    return character_data

@app.route("/delete_character/<char_name>", methods=["POST"])
def delete_character(char_name):
    json_filename = f"file/{char_name}.json"

    # 删除JSON文件
    if os.path.exists(json_filename):
        os.remove(json_filename)
        return f"角色 {char_name} 已成功删除！"
    else:
        return f"角色 {char_name} 不存在或已被删除。"

def num_random(i,x):
    num = 0
    for i in range(1,i+1):
        m = random.randint(1,x)
        num += m
    return num


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)