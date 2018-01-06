# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

#from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_Dialog import Ui_Dialog
import math


class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        '''以下為使用者自行編寫程式碼區'''
        self.display.setText('0')
        self.zero.clicked.connect(self.digitClicked)
        number = [self.one, self.two, self.three, self.four, \
            self.five, self.six, self.seven, self.eight, self.nine]
        for i in number:
            i.clicked.connect(self.digitClicked)
        plus_minus = [self.plusButton,  self.minusButton]
        for i in plus_minus:
            i.clicked.connect(self.additiveOperatorClicked)
        multiply_divide = [self.timesButton,  self.divisionButton]
        for i in multiply_divide:
            i.clicked.connect(self.multiplicativeOperatorClicked)
        self.clearAllButton.clicked.connect(self.clearAll)
        self.equalButton.clicked.connect(self.equalClicked)
        self.pointButton.clicked.connect(self.pointClicked)
        self.backspaceButton.clicked.connect(self.backspaceClicked)
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.pendingAdditiveOperator = ''
        self.pendingMultiplicativeOperator = ''
        unaryOperator = [self.squareRootButton, self.powerButton,  self.reciprocalButton ]
        for i in unaryOperator:
            i.clicked.connect(self.unaryOperatorClicked)
        self.clearMemoryButton.clicked.connect(self.clearMemory)
        self.readMemoryButton.clicked.connect(self.readMemory)
        self.setMemoryButton.clicked.connect(self.setMemory)
        self.sumInMemory = 0.0
        self.addToMemoryButton.clicked.connect(self.addToMemory)
        self.clearButton.clicked.connect(self.clear)
        self.changeSignButton.clicked.connect(self.changeSignClicked)
        self.wait = True
        
        #self.temp = 0
        
        
    def digitClicked(self):
        '''
        使用者按下數字鍵, 必須能夠累積顯示該數字
        當顯示幕已經為 0, 再按零不會顯示 00, 而仍顯示 0 或 0.0
        
        '''
        #pass
        clickedButton = self.sender()
        digitValue = int(clickedButton.text())
        if self.display.text() == '0' and digitValue == 0.0:
            return
        if self.wait:
            self.display.clear()
            self.wait = False
            

        self.display.setText(self.display.text() + str(digitValue))
        
    def unaryOperatorClicked(self):
        '''單一運算元按下後處理方法'''
        #pass
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())
 
        if clickedOperator == "Sqrt":
            if operand < 0.0:
                self.abortOperation()
                return
 
            result = math.sqrt(operand)
        elif clickedOperator == "X^2":
            result = math.pow(operand, 2.0)
        elif clickedOperator == "1/x":
            if operand == 0.0:
                self.abortOperation()
                return
 
            result = 1.0 / operand
 
        self.display.setText(str(result))
        self.wait = True
        
    def additiveOperatorClicked(self):
        '''加或減按下後進行的處理方法'''
        #pass
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())
        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
 
            self.display.setText(str(self.factorSoFar))
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''
            
        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return
                
            self.display.setText(str(self.sumSoFar))
        else:
            self.sumSoFar = operand
            
        self.pendingAdditiveOperator = clickedOperator
        
        self.wait = True
    
        #self.display.clear()
        
    def multiplicativeOperatorClicked(self):
        '''乘或除按下後進行的處理方法'''
        #pass
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())
        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
                
            self.display.setText(str(self.factorSoFar))
        else:
            self.factorSoFar = operand
            
        self.pendingMultiplicativeOperator = clickedOperator
        self.wait = True
        
    def equalClicked(self):
        '''等號按下後的處理方法'''
        #pass
        operand = float(self.display.text())
        
        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''
        
        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return
            self.pendingAdditiveOperator = ''
        else:
            self.sumSoFar = operand
 
        self.display.setText(str(self.sumSoFar))
        self.sumSoFar = 0.0
        
        self.wait = True
        
        
    def calculate(self, rightOperand, pendingOperator):
        if pendingOperator == "+":
            self.sumSoFar += rightOperand
 
        elif pendingOperator == "-":
            self.sumSoFar -= rightOperand
        
        elif pendingOperator == "*":
            self.factorSoFar *= rightOperand
 
        elif pendingOperator == "/":
            if rightOperand == 0.0:
                return False
                
            self.factorSoFar /= rightOperand  
            
        return True
 
        #self.display.setText(str(self.temp + float(self.display.text())))
        
    def pointClicked(self):
        '''小數點按下後的處理方法'''
        #pass
        if self.wait:
            self.display.setText('0')
 
        if "." not in self.display.text():
            self.display.setText(self.display.text() + ".")
 
        self.wait = False
        
    def changeSignClicked(self):
        '''變號鍵按下後的處理方法'''
        pass
        
    def backspaceClicked(self):
        '''回復鍵按下的處理方法'''
        #pass
        if self.wait:
            return
        text = self.display.text()[:-1]
        if not text:
            text = '0'
            self.wait = True
            
        self.display.setText(text)   
        
    def clear(self):
        '''清除鍵按下後的處理方法'''
        pass
        
    def clearAll(self):
        '''全部清除鍵按下後的處理方法'''
        #pass
        self.sumSoFar = 0.0
        self.pendingAdditiveOperator = ''
        self.display.setText('0')
        self.wait = True
        
    def clearMemory(self):
        '''清除記憶體鍵按下後的處理方法'''
        #pass
        self.sumInMemory = 0.0
        
    def readMemory(self):
        '''讀取記憶體鍵按下後的處理方法'''
        #pass
        self.display.setText(str(self.sumInMemory))
        self.wait = True
        
    def setMemory(self):
        '''設定記憶體鍵按下後的處理方法'''
        #pass
        self.equalClicked()
        self.sumInMemory = float(self.display.text())
        
    def addToMemory(self):
        '''放到記憶體鍵按下後的處理方法'''
        #pass
        self.equalClicked()
        self.sumInMemory += float(self.display.text())
 
        
    def createButton(self):
        ''' 建立按鍵處理方法, 以 Qt Designer 建立對話框時, 不需要此方法'''
        pass
        
    def abortOperation(self):
        '''中斷運算'''
        pass
        
    #def calculate(self):
        '''計算'''
        pass
