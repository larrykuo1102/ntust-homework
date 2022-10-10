

# --------------------------Parser Information--------------------------
# I.    object code 8 bits
#       01                                                                   2                                   34567
#       00(universal) 01(Application) 10(context-specific) 11(Private)      1(sequence, set, choice) 0(value)    tab number
#       a1(1010 0001)            81(1000 0001)

# II.   length 3 types
#       1. short definite -> 2 bytes length value
#       2. long definite -> start with 81 (1000 0001) *first bit has to be 1
#       3. infinite 

# III.  X length content

# --------------------------End--------------------------

# def getoneByte( hex_value ) : # 
#     pass

# def calculate_hex( hex_value ) : # get a byte value and translate to binary -> return 
#     binary_value = b''
    
#     return binary_value

def asn_1_parser( value ) -> dict : # make data to be tag+length+value
    data = {}
    
    return data


def Parser( content : str ) -> dict : 
    mms = []
    '''
    data = {
        tag : int,
        length : int,
        value : str
    }
    '''
    
    data = asn_1_parser(content)
    # PDU MMS
    
    if data['tag'] == 'a0' :
        confirmed_RequestPDU( data['value'] )
    elif data['tag'] == 'a1' :
        confirmed_ResponsePDU( data['value'] ) 
    
    
    return mms

def confirmed_RequestPDU( content ) :
    data = asn_1_parser(content)
    pass

def confirmed_ResponsePDU( content ) :
    data = asn_1_parser(content)
    
    pass



