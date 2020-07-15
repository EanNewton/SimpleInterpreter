#!/bin/python3
'''
Based on:
https://ruslanspivak.com/lsbasi-part1/
'''
''' 
Token types

EOF token is used to indicate that
there is no more input left for lexical analysis
'''

INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

class Token(object):
    def __init__(self, type, value):
        #token type: INTEGER, PLUS, MINUS, or EOF
        self.type = type
        #token value: 0-9, +, - or None
        self.value = value
    
    def __str__(self):
        '''String representation of the class instance.

        Examples:
        Token(INTEGER, 3)
        Token(PLUS, '+')
        '''
        return 'Token({type}, {value})'.format(
            type = self.type,
            value = repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        #client string input, e.g. "3+5"
        self.text = text
        #self.pos is an index into self.text
        self.pos = 0
        #current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        '''
        Lexical analyzer (aka scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One Token at a time.
        '''
        text = self.text

        #if self.pos index past the end of self.text
        #if so, then return EOF token because there is no more
        #input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)
        
        #get a character at the position self.pos and decide
        #what token to create based on the single character
        current_char = text[self.pos]

        #if the character is a digit then convert it to 
        #integer, create an INTEGER token, increment self.pos
        #index to point to the next character after the digit,
        #and return the INTEGER token
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        elif current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token
        
        elif current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token
        
        else:
            self.error()

    def consume(self, token_type):
        '''
        Compare the current token type with the passed token
        type and if they match consume the current token
        and assign the next token to the self.current_token,
        otherwise raise an exception
        '''
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
    
    def expr(self):
        '''expr -> INTEGER OP INTEGER'''
        #set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        #we expect the current token to be an integer
        #and possibly following tokens
        left, right = [], []
        while(self.current_token.type == INTEGER):
            left.append(self.current_token)
            self.consume(INTEGER)
        l_val, pos = 0, 1
        #take all integers to this point in reverse order
        #and combine them
        for each in left[::-1]:
            l_val += each.value * pos
            pos *= 10

        #we expect the current token to be a '+' or '-' token
        op = self.current_token
        self.consume(op.type)

        #we expect the current token to be an integer
        while(self.current_token.type == INTEGER):
            right.append(self.current_token)
            self.consume(INTEGER)
        r_val, pos = 0, 1
        for each in right[::-1]:
            r_val += each.value * pos
            pos *= 10
        #after the above call the self.current_token is set to
        #EOF token

        '''
        At this point INTEGER OP INTEGER sequence of tokens
        has been successfully found and the method can just
        return the result of OP'ing two integers, thus
        effectively interpreting client input
        '''
        if op.type == PLUS:
            result = l_val + r_val
        elif op.type == MINUS:
            result = l_val - r_val
        return result

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text.replace(' ', ''))
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()