# -*- coding: utf-8 -*-

import CaboCha
import gc

class CnlpREI:
    # コンストラクタ
    def __init__(self):
        self.wakati_data = []
        self.nlp_text = ""
        self.cabocha_text = []

    # デストラクタ
    def __del__(self):
        del self.cabocha
        gc.collect()

    # 形態素解析
    def nlp(self, text):
        self.nlp_text = text

        #かかり受け解析
        self.cabocha = CaboCha.Parser()
        self.tree = self.cabocha.parse(self.nlp_text)  #textのデータ構造を格納

        for i in range(0, self.tree.size()):
                self.cabocha_text.append(self.tree.token(i).surface)

        return self.cabocha_text
