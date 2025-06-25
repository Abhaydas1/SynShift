from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Translation Logic
class Translator:
    """Base class for language translation."""
    def translate(self, code):
        raise NotImplementedError("Subclasses should implement this!")

# Python to Other Languages
class PythonToC(Translator):
    def translate(self, code):
        code = code.replace("print(", 'printf("').replace(")", '");')
        code = code.replace("if ", "if (").replace(":", ") {")
        code = code.replace("else:", "} else {")
        return f"#include <stdio.h>\nint main() {{\n{code}\nreturn 0;\n}}"

class PythonToCpp(Translator):
    def translate(self, code):
        code = code.replace("print(", 'std::cout << ').replace(")", " << std::endl;")
        code = code.replace("if ", "if (").replace(":", ") {")
        code = code.replace("else:", "} else {")
        return f"#include <iostream>\nusing namespace std;\nint main() {{\n{code}\nreturn 0;\n}}"

class PythonToJava(Translator):
    def translate(self, code):
        code = code.replace("print(", 'System.out.println(').replace(")", ");")
        code = code.replace("if ", "if (").replace(":", ") {")
        code = code.replace("else:", "} else {")
        return f"public class Main {{\n    public static void main(String[] args) {{\n{code}\n    }}\n}}"

class PythonToJavaScript(Translator):
    def translate(self, code):
        code = code.replace("print(", "console.log(").replace(")", ");")
        code = code.replace("if ", "if (").replace(":", ") {")
        code = code.replace("else:", "} else {")
        return f"function main() {{\n{code}\n}}\nmain();"

class PythonToCSharp(Translator):
    def translate(self, code):
        code = code.replace("print(", "Console.WriteLine(").replace(")", ");")
        code = code.replace("if ", "if (").replace(":", ") {")
        code = code.replace("else:", "} else {")
        return f"using System;\nclass Program {{\n    static void Main() {{\n{code}\n    }}\n}}"

# Other Languages to Python
class CToPython(Translator):
    def translate(self, code):
        code = code.replace("printf(", "print(").replace('");', ")")
        code = code.replace("if (", "if ").replace(") {", ":")
        code = code.replace("} else {", "else:")
        return f"# Python Code\n{code}"

class CppToPython(Translator):
    def translate(self, code):
        code = code.replace("std::cout << ", "print(").replace(" << std::endl;", ")")
        code = code.replace("if (", "if ").replace(") {", ":")
        code = code.replace("} else {", "else:")
        return f"# Python Code\n{code}"

class JavaToPython(Translator):
    def translate(self, code):
        code = code.replace("System.out.println(", "print(").replace(");", ")")
        code = code.replace("if (", "if ").replace(") {", ":")
        code = code.replace("} else {", "else:")
        return f"# Python Code\n{code}"

class JavaScriptToPython(Translator):
    def translate(self, code):
        code = code.replace("console.log(", "print(").replace(");", ")")
        code = code.replace("if (", "if ").replace(") {", ":")
        code = code.replace("} else {", "else:")
        return f"# Python Code\n{code}"

class CSharpToPython(Translator):
    def translate(self, code):
        code = code.replace("Console.WriteLine(", "print(").replace(");", ")")
        code = code.replace("if (", "if ").replace(") {", ":")
        code = code.replace("} else {", "else:")
        return f"# Python Code\n{code}"

# Translator Mapping
TRANSLATORS = {
    ("Python", "C"): PythonToC,
    ("Python", "C++"): PythonToCpp,
    ("Python", "Java"): PythonToJava,
    ("Python", "JavaScript"): PythonToJavaScript,
    ("Python", "C#"): PythonToCSharp,
    ("C", "Python"): CToPython,
    ("C++", "Python"): CppToPython,
    ("Java", "Python"): JavaToPython,
    ("JavaScript", "Python"): JavaScriptToPython,
    ("C#", "Python"): CSharpToPython,
}

def translate_code(source_lang, target_lang, code):
    if source_lang == target_lang:
        return "// No translation needed. Same source and target language.\n" + code

    translator_class = TRANSLATORS.get((source_lang, target_lang))
    if not translator_class:
        return "// Translation for this combination is not yet supported."

    translator = translator_class()
    return translator.translate(code)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    source_lang = data.get("source_lang")
    target_lang = data.get("target_lang")
    code = data.get("code")

    translated_code = translate_code(source_lang, target_lang, code)
    return jsonify({"translated_code": translated_code})

if __name__ == "__main__":
    app.run(debug=True)
