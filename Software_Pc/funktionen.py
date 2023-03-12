import copy


def compelier(blocks):
    blocksQuelle = copy.deepcopy(blocks)
    blockProgram =[]
        
    fertig = True

    while blocksQuelle:
        blockVomSpeicher = blocksQuelle.pop()

        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'ZUW':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 'OUT':blockVomSpeicher['OUT'], 'IN1': blockVomSpeicher['in1']}
                blockProgram.append(blockP)

        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'INPUT':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 'OUT':blockVomSpeicher['out1'], 'IN1': blockVomSpeicher['in1']}
                blockProgram.append(blockP)

        #Format {'B3':'TON', 'OUT':'B2-I1', 'IN1': 'B4', 'TONNR': 'TON1', 'PARAMETER1': 2.5}
        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'TON':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 
                            'OUT':blockVomSpeicher['out1'], 'IN1': blockVomSpeicher['in1'],
                            'TONNR':blockVomSpeicher['timerNr'], 'PARAMETER1': blockVomSpeicher['parameter1']}
                blockProgram.append(blockP)
        
        #Format {'B3':'TOF', 'OUT':'B2-I1', 'IN1': 'B4', 'TOFNR': 'TON1', 'PARAMETER1': 2.5}
        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'TOF':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 
                            'OUT':blockVomSpeicher['out1'], 'IN1': blockVomSpeicher['in1'],
                            'TOFNR':blockVomSpeicher['timerNr'], 'PARAMETER1': blockVomSpeicher['parameter1']}
                blockProgram.append(blockP)
        
        #{'B17':'CUD', 'OUT':'B14-I1', 'IN1': 'I2', 'IN2': 'I1', 'IN3': '',
            #'CUDNR': 'CUD1', 'PARAMETER1': 0, 'PARAMETER2': 3}
        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'CUD':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 
                            'OUT':blockVomSpeicher['out1'],
                             'IN1': blockVomSpeicher['in1'],
                             'IN2': blockVomSpeicher['in2'],
                             'IN3': blockVomSpeicher['in3'],
                            'CUDNR':blockVomSpeicher['cudNr'],
                             'PARAMETER1': blockVomSpeicher['parameter1'],
                             'PARAMETER2': blockVomSpeicher['parameter2']}
                blockProgram.append(blockP)

        #{'B17':'LT', 'OUT':'B14-I1', 'IN1': 'CUD1', 'IN2': 'TON1'}
        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'LT':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 
                            'OUT':blockVomSpeicher['out1'],
                             'IN1': blockVomSpeicher['in1'],
                             'IN2': blockVomSpeicher['in2']}
                blockProgram.append(blockP)

        #{'B17':'LIT', 'OUT':'B14-I1', 'IN1': 'CUD1', 'IN2': 'TON1'}
        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'LIT':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 
                            'OUT':blockVomSpeicher['out1'],
                             'IN1': blockVomSpeicher['in1'],
                             'IN2': blockVomSpeicher['in2']}
                blockProgram.append(blockP)
        
        #{'B17':'GT', 'OUT':'B14-I1', 'IN1': 'CUD1', 'IN2': 'TON1'}
        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'GT':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 
                            'OUT':blockVomSpeicher['out1'],
                             'IN1': blockVomSpeicher['in1'],
                             'IN2': blockVomSpeicher['in2']}
                blockProgram.append(blockP)

        #{'B17':'GIT', 'OUT':'B14-I1', 'IN1': 'CUD1', 'IN2': 'TON1'}
        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'GIT':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 
                            'OUT':blockVomSpeicher['out1'],
                             'IN1': blockVomSpeicher['in1'],
                             'IN2': blockVomSpeicher['in2']}
                blockProgram.append(blockP)

        #{'B17':'IT', 'OUT':'B14-I1', 'IN1': 'CUD1', 'IN2': 'TON1'}
        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'IT':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 
                            'OUT':blockVomSpeicher['out1'],
                             'IN1': blockVomSpeicher['in1'],
                             'IN2': blockVomSpeicher['in2']}
                blockProgram.append(blockP)

        #{'B17':'NIT', 'OUT':'B14-I1', 'IN1': 'CUD1', 'IN2': 'TON1'}
        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'NIT':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 
                            'OUT':blockVomSpeicher['out1'],
                             'IN1': blockVomSpeicher['in1'],
                             'IN2': blockVomSpeicher['in2']}
                blockProgram.append(blockP)

        #{'B17':'ADD', 'OUT':'MW2', 'IN1': 'B2', 'IN2': 'TON1', 'IN3': 'TON2'}
        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'ADD':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 
                            'OUT':blockVomSpeicher['out1'],
                             'IN1': blockVomSpeicher['in1'],
                             'IN2': blockVomSpeicher['in2'],
                             'IN3': blockVomSpeicher['in3']}
                blockProgram.append(blockP)

        #{'B17':'ADD', 'OUT':'MW2', 'IN1': 'B2', 'IN2': 'TON1', 'IN3': 'TON2'}
        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'SUB':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 
                            'OUT':blockVomSpeicher['out1'],
                             'IN1': blockVomSpeicher['in1'],
                             'IN2': blockVomSpeicher['in2'],
                             'IN3': blockVomSpeicher['in3']}
                blockProgram.append(blockP)

        #{'B17':'ADD', 'OUT':'MW2', 'IN1': 'B2', 'IN2': 'TON1', 'IN3': 'TON2'}
        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'MUL':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 
                            'OUT':blockVomSpeicher['out1'],
                             'IN1': blockVomSpeicher['in1'],
                             'IN2': blockVomSpeicher['in2'],
                             'IN3': blockVomSpeicher['in3']}
                blockProgram.append(blockP)

        #{'B17':'ADD', 'OUT':'MW2', 'IN1': 'B2', 'IN2': 'TON1', 'IN3': 'TON2'}
        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'DIV':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 
                            'OUT':blockVomSpeicher['out1'],
                             'IN1': blockVomSpeicher['in1'],
                             'IN2': blockVomSpeicher['in2'],
                             'IN3': blockVomSpeicher['in3']}
                blockProgram.append(blockP)

         #{'B17':'MOVE', 'OUT':'MW2', 'IN1': 'B2', 'IN2': 'TON1'}
        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'MOVE':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 
                            'OUT':blockVomSpeicher['out1'],
                             'IN1': blockVomSpeicher['in1'],
                             'IN2': blockVomSpeicher['in2']}
                blockProgram.append(blockP)

        #Format {'B14':'SR', 'OUT':'B13-I1', 'IN1': 'B15', 'IN2': 'B16', 'SRNR': 'SR1'}
        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'SR':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 
                            'OUT':blockVomSpeicher['out1'], 'IN1': blockVomSpeicher['in1'], 'IN2': blockVomSpeicher['in2'],
                            'SRNR':blockVomSpeicher['srNr']}
                blockProgram.append(blockP)

        #Format {'B14':'IP', 'OUT':'B13-I1', 'IN1': 'B15', 'IPNR': 'IP1'}
        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'IP':
                blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 
                            'OUT':blockVomSpeicher['out1'], 'IN1': blockVomSpeicher['in1'],
                            'IPNR':blockVomSpeicher['ipNr']}
                blockProgram.append(blockP)

        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'INV':
                if 'in1' in blockVomSpeicher:
                    blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 'OUT':blockVomSpeicher['out1'], 'IN1': blockVomSpeicher['in1']}
                blockProgram.append(blockP)

        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'OR':
                if 'in1' in blockVomSpeicher:
                    blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 'OUT':blockVomSpeicher['out1'], 'IN1': blockVomSpeicher['in1']}
                if 'in2' in blockVomSpeicher:
                    blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 'OUT':blockVomSpeicher['out1'], 'IN1': blockVomSpeicher['in1'], 'IN2': blockVomSpeicher['in2']}
                if 'in3' in blockVomSpeicher:
                    blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 'OUT':blockVomSpeicher['out1'], 'IN1': blockVomSpeicher['in1'], 'IN2': blockVomSpeicher['in2'], 'IN3': blockVomSpeicher['in3']}
                blockProgram.append(blockP)

        if 'typ' in blockVomSpeicher:
            if blockVomSpeicher['typ'] == 'AND':
                if 'in1' in blockVomSpeicher:
                    blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 'OUT':blockVomSpeicher['out1'], 'IN1': blockVomSpeicher['in1']}
                if 'in2' in blockVomSpeicher:
                    blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 'OUT':blockVomSpeicher['out1'], 'IN1': blockVomSpeicher['in1'], 'IN2': blockVomSpeicher['in2']}
                if 'in3' in blockVomSpeicher:
                    blockP ={blockVomSpeicher['blockNr']:blockVomSpeicher['typ'], 'OUT':blockVomSpeicher['out1'], 'IN1': blockVomSpeicher['in1'], 'IN2': blockVomSpeicher['in2'], 'IN3': blockVomSpeicher['in3']}
                blockProgram.append(blockP)
    
        if not blocksQuelle:
            fertig = False

    blockProgram.reverse()
    return blockProgram

    #{'B1': 'ZUW', 'OUT': 'Q1', 'IN1': 'B2'}, {'B2': 'AND', 'OUT': 'B1-I1', 'IN1': 'B3', 'IN2': 'B4', 'IN3': 'B5'}
