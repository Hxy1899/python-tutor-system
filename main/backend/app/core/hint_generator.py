class HintGenerator:
    """
    Generates guided hints based on error types.
    """
    
    HINTS = {
        "SyntaxError": [
            "仔细检查代码中的括号、引号、冒号是否成对出现且正确输入。",
            "确认关键字拼写是否正确，缩进是否符合规范。",
            "查看错误提示行号的前后代码，是否有漏写的标点符号。"
        ],
        "IndentationError": [
            "Python中缩进是非常重要的。检查代码块的缩进是否一致。",
            "确保if/for/while/def语句后的代码块缩进正确。",
            "统一使用4个空格或1个Tab作为缩进，不要混用。"
        ],
        "NameError": [
            "检查变量名是否拼写正确，Python是区分大小写的。",
            "确认变量在使用前已经赋值，函数是否在定义后调用。",
            "如果你在函数内部使用变量，确认该变量是否已在该范围内定义。"
        ],
        "TypeError": [
            "检查数据类型是否匹配。例如，你是否在尝试对数字和字符串进行加法运算？",
            "确认函数的参数数量和类型是否正确。",
            "如果使用了内置函数，查阅其文档确认期望的输入类型。"
        ],
        "ZeroDivisionError": [
            "检查除法运算中的分母是否可能为0。",
            "考虑使用if语句检查分母是否为0，以避免此类错误。"
        ],
        "IndexError": [
            "列表/字符串的索引超出了范围。确认你的索引是否在有效长度内。",
            "记住，Python中的索引是从0开始的。"
        ],
        "KeyError": [
            "字典中不存在你尝试访问的键。检查键名是否正确。",
            "可以使用.get()方法来安全地访问字典中的键。"
        ],
        "LogicalError": [
            "代码运行成功但结果不符合预期。检查逻辑控制流程是否正确。",
            "尝试在关键位置添加打印语句，查看变量的值是否符合预期。",
            "思考你的算法实现步骤是否完全符合题目要求。"
        ]
    }

    @staticmethod
    def generate(error_type: str, code: str = "") -> str:
        """
        Generate a guided hint based on the error type.
        """
        # Find hints based on the error type. 
        # ML model might return RXX: Name or just name.
        
        # Normalize error type
        normalized_type = error_type
        if ":" in error_type:
            normalized_type = error_type.split(":")[1].strip()
        
        # Get hint list
        hints = HintGenerator.HINTS.get(normalized_type, ["请仔细检查代码逻辑。"])
        
        # Join hints into a string (can be randomized or picked based on complexity)
        return "\n".join([f"- {h}" for h in hints])
