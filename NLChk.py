#=============================================================================================#
import re
import sys
#=============================================================================================#
def main():
    global ivscollect,natcollect
    ivscollect = re.compile('\d+')
    natcollect = re.compile('[a-zA-z]+')
    infograbber()
    looplist = ivsloopgenerator()
    print('Grabbing possible IV seeds:')
    seedlist = existchk(looplist)
    print('Done!')
    if seedlist == []:
        print('No IV/Nature combos found with entered criteria; program restarting.\n')
    else:
        print('Comparing seeds versus NLs:')
        for data in seedlist:
            resultstr = casehandler(data[0])
            if resultstr[0:1] == 'H':
                var_name = "NLChk_Valid"
                sys.stdout.write('.')
                sys.stdout.flush()
            else:
                var_name = "NLChk_Invalid"
            var_name = var_name + ".txt"
            final_result = data[1] + ',' + data[2] + ',' + data[3] + ',' + resultstr
            outputtotxt(var_name,final_result)
#=============================================================================================#
def infograbber():
    print('\nEnter desired pokemon name; NLChk currently only supports 1 pokemon per search,')
    print('though that may or may not change in future versions of this program.\n')
    valid = False
    while valid == False:
        valid = pokeinput()
    print('\nEnter desired search limits for IVs (ordering = HP->Atk->Def->SpA->SDf->Spe).')
    print('Any non-numeric characters can separate IVs (for both lower and upper limits).')
    print('Note that NLChk will only use the first 6 input IVs, despite accepting more.\n')
    valid = False
    while valid == False:
        valid = ivsinput_lower()
    print('\nEnter desired nature(s) to search for; for multiple entries, seperate each with')
    print('a non-alphabetical character (cannot contain anything in a-z or A-Z). Beyond')
    print('that, it doesn\'t matter what you use to seperate them; NLChk will do the rest.\n')
    valid = False
    while valid == False:
        valid = natinput()
#=============================================================================================#
def pokeinput():
    global pokelist,poke_input
    pokelist = []
    poke_input = (raw_input('Desired Pokemon = ')).upper()
    valid = False
    try:
        pokelist = POKEMON[poke_input]
    except KeyError:
        print('\n\"%s\" is not a valid pokemon for use with NLChk. Please check the README' % poke_input)
        print('for what is currently supported / unsupported and planned for future versions.\n')
    if pokelist != []:
        valid = True
    return valid
#=============================================================================================#
def natinput():
    global confirmednats
    confirmednats = []
    nat_input = raw_input('Desired Nature(s) = ')
    desirednatlist = natcollect.findall(nat_input)
    if desirednatlist == []:
        print('No natures have been entered; please enter valid nature input.\n')
        valid = False
    else:
        for nat in desirednatlist:
            nature = nat.upper()
            try:
                nature = NATUREVERSE[nature]
                confirmednats.append(nature)
            except KeyError:
                print('\"%s\" is not a valid nature; please enter an all-valid nature input.\n' % desirednatlist[nat])
                valid = False
                break
        else:
            valid = True
    return valid
#=============================================================================================#
def ivsinput_lower():
    global ivs_lower
    ivs_lower = []
    ivs_input = raw_input('Lower IV Limits = ')
    desiredivslist = ivscollect.findall(ivs_input)
    valid = False
    if desiredivslist == []:
        print('No Lower IVs entered! please enter a valid IV spread.\n')
    else:
        for ivs in range(6):
            try:
                if len(desiredivslist[ivs]) > 2:
                    raise IndexError
                try:
                    intivs = int(desiredivslist[ivs],10)
                    if(intivs > 31 or intivs < 0):
                        raise IndexError
                    else:
                        ivs_lower.append(intivs)
                except ValueError:
                    raise IndexError
            except IndexError:
                print('Invalid Lower IV input; please enter a valid IV spread.\n')
                break
        else:
            valid = ivsinput_upper()
    return valid
#=============================================================================================#
def ivsinput_upper():
    global ivs_upper
    ivs_upper = []
    valid = False
    ivs_input = raw_input('Upper IV Limits = ')
    desiredivslist = ivscollect.findall(ivs_input)
    if desiredivslist == []:
        print('No Upper IVs entered! please enter a valid pair of IV spreads.\n')
    else:
        for ivs in range(6):
            try:
                if len(desiredivslist[ivs]) > 2:
                    raise IndexError
                try:
                    intivs = int(desiredivslist[ivs],10)
                    if(intivs > 31 or intivs < 0):
                        raise IndexError
                    else:
                        ivs_upper.append(intivs)
                except ValueError:
                    raise IndexError
            except IndexError:
                print('Invalid Upper IV input; please enter a valid pair of IV spreads.\n')
                break
        else:
            for chk in range(6):
                try:
                    a = ivs_upper[chk]
                    b = ivs_lower[chk]
                    if b > a:
                        raise ValueError
                except ValueError:
                    print('Cannot search with lower limit greater than upper. Please re-enter both.\n')
                    break
            else:
                valid = True
    return valid
#=============================================================================================#
def ivsloopgenerator():
    looplist = []
    for g in range(6):
        temp = []
        for h in range(ivs_lower[g],(ivs_upper[g]+1),1):
            temp.append(h)
        looplist.append(temp)
    return looplist
#=============================================================================================#
def x8calc(ivL,ivM,ivH):
    x8 = ivL + (ivM << 5) + (ivH << 10)
    return x8
#=============================================================================================#
def existchk(looplist):
    dotchk = 0
    hp = looplist[0]
    at = looplist[1]
    df = looplist[2]
    sa = looplist[3]
    sd = looplist[4]
    sp = looplist[5]
    spos = []
    for a in hp:
        hpiv = a
        for b in at:
            ativ = b
            for c in df:
                dfiv = c
                for d in sa:
                    saiv = d
                    for e in sd:
                        sdiv = e
                        for f in sp:
                            spiv = f
                            x8 = x8calc(hpiv,ativ,dfiv)
                            x8_2 = x8 ^ 0x8000
                            ex8 = x8calc(sdiv,saiv,spiv)
                            ex8_2 = ex8 ^ 0x8000
                            for cnt in range(0x1fffe):
                                x_test = cnt & 1
                                if x_test == 0:
                                    ivs_1 = x8
                                else:
                                    ivs_1 = x8_2
                                if cnt < 0xffff:
                                    seed = (ivs_1 << 16) + (cnt & 0xffff)
                                else:
                                    seed = (ivs_1 << 16) + ((cnt+1) & 0xffff)
                                ivs_2 = prngbackward(seed,1) >> 16
                                if(ivs_2 == ex8 or ivs_2 == ex8_2):
                                    iseed = prngbackward(seed,2)
                                    tf,nat = natchk(iseed)
                                    if tf == True:
                                        hexiseed = hexify(iseed)
                                        ivstr = ivstrconstruct(hpiv,ativ,dfiv,saiv,sdiv,spiv)
                                        cont = [iseed,hexiseed,NATURES[nat],ivstr]
                                        spos.append(cont)
                                        if (dotchk & 0x1f) == 0:
                                            sys.stdout.write('.')
                                            sys.stdout.flush()
                                        dotchk = dotchk + 1
    return spos
#=============================================================================================#
def ivstrconstruct(hpiv,ativ,dfiv,saiv,sdiv,spiv):
    temp = [hpiv,ativ,dfiv,saiv,sdiv,spiv]
    rcomp = []
    for z in range(6):
        iv = str(temp[z])
        if len(iv) < 2:
            iv = '0' + iv
        rcomp.append(iv)
    ivstr = '%s/%s/%s/%s/%s/%s' % (rcomp[0],rcomp[1],rcomp[2],rcomp[3],rcomp[4],rcomp[5])
    return ivstr
#=============================================================================================#
def natchk(initseed):
    s = prngforward(initseed,4)
    pidh = s >> 16
    s = prngforward(s,1)
    pidl = s >> 16
    pid = (pidh << 16) + pidl
    nat = pid % 25
    for n in confirmednats:
        if nat == n:
            return True, nat
    return False, 'N/A'
#=============================================================================================#
def hexify(seed):
    hseed = hex(seed)
    hseed = hseed[2:]
    while len(hseed) < 8:
        hseed = '0' + hseed
    hseed = '0x' + hseed
    return hseed
#=============================================================================================#
def casehandler(seed):
    name = poke_input
    nlnum = pokelist[0]
    pkmnpos = pokelist[1]
    if nlnum == 0:
        frv_str = RESULT[0] + name + REASON[0]
        return frv_str
    elif nlnum == 1:
        if pkmnpos == 1:
            pf_str,r_str = sNL_1S(seed)
            frv_str = pf_str + name + r_str
            return frv_str
        else:
            pf_str,r_str = sNL_2S(seed)
            frv_str = pf_str + name + r_str
            return frv_str
    else:
        if pkmnpos == 1:
            pf_str,r_str = mNL_1S(seed)
            frv_str = pf_str + name + r_str
            return frv_str
        else:
            pf_str,r_str = mNL_2S(seed)
            frv_str = pf_str + name + r_str
            return frv_str
#=============================================================================================#
def sNL_1S(seed):
    s = prngbackward(seed,1)
    gv,nl,s = gvnlchkB(s)
    test = gvcomp(gv,pokelist[2],pokelist[3])
    if test == True and nl == pokelist[4]:
        pfstring = RESULT[0]
        rstring = REASON[1]
        return pfstring,rstring
    else:
        pfstring = RESULT[1]
        rstring = REASON[3]
        return pfstring,rstring
#=============================================================================================#
def sNL_2S(seed):
    j,s = sstest(seed)
    if j == -1:
        pfstring = RESULT[1]
        rstring = REASON[5]
        return pfstring,rstring
    else:
        pfstring = RESULT[0]
        rstring = REASON[2]+SETUP[j]
        return pfstring,rstring
#=============================================================================================#
def mNL_1S(seed):
    timesB = []
    timesF = []
    for v in range(0,pokelist[0],1):
        n = (v * 3) + 4
        nltest = pokelist[n]
        gvmin = pokelist[n-2]
        gvmax = pokelist[n-1]
        if v == 0:
            s = prngbackward(seed,1)
            gv,nl,s = gvnlchkB(s)
            test = gvcomp(gv,pokelist[2],pokelist[3])
            if (test == True and nl == pokelist[4]):
                timesB.append(7)
            else:
                pfstring = RESULT[1]
                rstring = REASON[3]
                return pfstring,rstring
        else:
            if nltest == -1:
                s = prngbackward(s,5)
                timesB.append(5)
            else:
                s = prngbackward(s,3)
                gv,nl,s = gvnlchkB(s)
                gvtf = gvcomp(gv,gvmin,gvmax)
                tb = False
                if(nl == nltest and gvtf == True):
                    tb = True
                tback = 0
                while tb == False:
                    tback = tback + 2
                    gv,nl,s = gvnlchkB(s)
                    gvtf = gvcomp(gv,gvmin,gvmax)
                    if(nl == nltest and gvtf == True):
                        tb = True
                timesB.append(tback+5)
    for x in range(pokelist[0],0,-1):
        n = (x * 3) + 1
        nltest = pokelist[n]
        gvmin = pokelist[n-2]
        gvmax = pokelist[n-1]
        if x == pokelist[0]:
            s = prngforward(s,1)
            timesF.append(7)
        else:
            if nltest == -1:
                s = prngforward(s,5)
                timesF.append(5)
            else:
                s = prngforward(s,3)
                gv,nl,s = gvnlchkF(s)
                gvtf = gvcomp(gv,gvmin,gvmax)
                tf = False
                if(nl == nltest and gvtf == True):
                    tf = True
                tforw = 0
                while tf == False:
                    tforw = tforw + 2
                    gv,nl,s = gvnlchkF(s)
                    gvtf = gvcomp(gv,gvmin,gvmax)
                    if(nl == nltest and gvtf == True):
                        tf = True
                timesF.append(tforw+5)
    countB = 0
    countF = 0
    for item in timesB:
        countB = countB + item
    for items in timesF:
        countF = countF + items
    if countB == countF:
        pfstring = RESULT[0]
        rstring = REASON[1]
        countstr = ' (%d,%d)' % (countB,countF)
        rstring = rstring + countstr
        return pfstring,rstring
    else:
        pfstring = RESULT[1]
        rstring = REASON[4]
        countstr = ' (%d,%d)' % (countB,countF)
        rstring = rstring + countstr
        return pfstring,rstring
#=============================================================================================#
def mNL_2S(seed):
    timesB = []
    timesF = []
    for z in range(0,pokelist[0],1):
        n = (z*3)+4
        nltest = pokelist[n]
        gvmin = pokelist[n-2]
        gvmax = pokelist[n-1]
        if z == 0:
            j,s = sstest(seed)
            if j == -1:
                pfstring = RESULT[1]
                rstring = REASON[5]
                return pfstring,rstring
            timesB.append(12+(j*2))
        else:
            if nltest == -1:
                s = prngbackward(s,5)
                timesB.append(5)
            else:
                s = prngbackward(s,3)
                gv,nl,s = gvnlchkB(s)
                gvtf = gvcomp(gv,gvmin,gvmax)
                tb = False
                if(nltest == nl and gvtf == True):
                    tb = True
                tback = 0
                while tb == False:
                    tback = tback + 2
                    gv,nl,s = gvnlchkB(s)
                    gvtf = gvcomp(gv,gvmin,gvmax)
                    if(nltest == nl and gvtf == True):
                        tb = True
                timesB.append(tback+5)
    for k in range(pokelist[0],0,-1):
        n = (k*3)+1
        nltest = pokelist[n]
        gvmin = pokelist[n-2]
        gvmax = pokelist[n-1]
        if k == pokelist[0]:
            s = prngforward(s,1)
            timesF.append(12+(j*2))
        else:
            if nltest == -1:
                s = prngforward(s,5)
                timesF.append(5)
            else:
                s = prngforward(s,3)
                gv,nl,s = gvnlchkF(s)
                gvtf = gvcomp(gv,gvmin,gvmax)
                tf = False
                if(nl == nltest and gvtf == True):
                    tf = True
                tforw = 0
                while tf == False:
                    tforw = tforw + 2
                    gv,nl,s = gvnlchkF(s)
                    gvtf = gvcomp(gv,gvmin,gvmax)
                    if(nl == nltest and gvtf == True):
                        tf = True
                timesF.append(tforw+5)
    countB = 0
    countF = 0
    for item in timesB:
        countB = countB + item
    for items in timesF:
        countF = countF + items
    if countB == countF:
        pfstring = RESULT[0]
        rstring = REASON[2]+SETUP[j]
        countstr = ' (%d,%d)' % (countB,countF)
        rstring = rstring + countstr
        return pfstring,rstring
    else:
        pfstring = RESULT[1]
        rstring = REASON[4]
        countstr = ' (%d,%d)' % (countB,countF)
        rstring = rstring + countstr
        return pfstring,rstring
#=============================================================================================#
def sstest(usrseed):
    s = prngbackward(usrseed,6)
    for j in range(3):
        gv,nl,s = gvnlchkB(s)
        test = gvcomp(gv,pokelist[2],pokelist[3])
        if(test == True and nl == pokelist[4]):
            return (j,s)
    return (-1,s)
#=============================================================================================#
def gvnlchkB(seed):
    s = prngbackward(seed,1)
    pidl = s >> 16
    s = prngbackward(s,1)
    pidh = s >> 16
    pid = (pidh << 16) + pidl
    gv = pid & 0xFF
    nl = pid % 25
    return (gv,nl,s)
#=============================================================================================#
def gvnlchkF(seed):
    s = prngforward(seed,1)
    pidh = s >> 16
    s = prngforward(s,1)
    pidl = s >> 16
    pid = (pidh << 16) + pidl
    gv = pid & 0xFF
    nl = pid % 25
    return (gv,nl,s)
#=============================================================================================#
def gvcomp(gvval,gvmin,gvmax):
    if(gvval >= gvmin and gvval <= gvmax):
        return True
    return False
#=============================================================================================#
def prngbackward(seed, times):
    s = seed
    for i in range(times):
        s = (s * 0xB9B33155 + 0xA170F641) & 0xFFFFFFFF
    return s
#=============================================================================================#
def prngforward(seed, times):
    s = seed
    for q in range(times):
        s = (s * 0x000343FD + 0x00269EC3) & 0xFFFFFFFF
    return s
#=============================================================================================#
def outputtotxt(txtname,string):
    txtf = open(txtname, 'a')
    txtf.write(string + '\n')
    txtf.close()
#=============================================================================================#
SETUP = {
    0:'first shadow pokemon IVs/Nature set.',
    1:'first shadow pokemon IVs/Nature unset.',
    2:'first shadow pokemon IVs/Nature unset + shiny PID reroll.'
    }
#=============================================================================================#
RESULT = {
    0:'Hypothetically valid IV/Nature combo for ',
    1:'Invalid IV/Nature combo for '
    }
#=============================================================================================#
REASON = {
    0:'; this pokemon has no NLs!',
    1:'; passes NL(s).',
    2:'; passes NL(s) with ',
    3:'; fails NL closest to target.',
    4:'; NLs will always result in earlier frame(s) than the intended target.',
    5:'; fails all possible 1st shadow combos for the closest NL.'
    }
#=============================================================================================#
POKEMON = {
    "SPINARAK":[2,1,128,255,6,0,127,12],
    "MAKUHITA":[2,1,0,127,18,128,255,6],
    "DUSKULL":[3,1,128,255,24,0,127,18,128,255,12],
    "FARFETCH'D":[3,1,128,255,24,0,127,0,128,255,12],
    "ALTARIA":[3,6,128,255,24,0,127,0,128,255,12],
    "KANGASKHAN":[3,1,0,255,12,0,127,18,0,255,0],
    "BANETTE":[3,6,0,255,12,0,127,18,0,255,0],
    "MAGMAR":[3,1,0,127,0,192,255,18,128,255,18],
    "PINSIR":[3,6,0,127,0,192,255,18,128,255,18],
    "RAPIDASH":[3,1,0,127,12,128,255,6,128,255,24],
    "MAGCARGO":[3,6,0,127,12,128,255,6,128,255,24],
    "HITMONCHAN":[3,1,0,127,18,0,127,6,128,255,24],
    "HITMONLEE":[4,1,0,127,24,0,255,6,0,127,12,128,255,18],
    "LICKITUNG":[2,1,0,255,6,128,255,24],
    "SCYTHER":[2,1,128,255,24,0,127,6],
    "CHANSEY":[2,6,128,255,24,0,127,6],
    "SOLROCK":[3,1,0,127,0,128,255,6,0,255,24],
    "GROWLITHE":[2,6,0,127,6,128,255,24],
    "BUTTERFREE":[3,6,0,127,0,128,255,6,0,191,12],
    "WEEPINBELL":[3,6,128,255,12,0,255,24,0,127,18],
    "HYPNO":[4,6,128,255,24,0,127,6,0,127,12,0,127,18],
    "SABLEYE":[3,6,0,127,18,0,127,6,128,255,24],
    "RATICATE":[3,1,128,255,18,-1,-1,-1,0,127,18],
    "STARMIE":[5,1,128,255,18,-1,-1,-1,0,127,0,128,255,6,0,255,24],
    "ELECTABUZZ":[3,1,0,127,18,0,127,6,64,255,24],
    "SNORLAX":[3,6,0,127,18,0,127,6,64,255,24],
    "MR. MIME":[4,6,0,127,6,128,255,24,128,255,18,128,255,18],
    "SALAMENCE":[1,6,0,127,6],
    "MAROWAK":[4,1,128,255,24,-1,-1,-1,-1,-1,-1,0,127,6],
    "LAPRAS":[4,6,128,255,24,-1,-1,-1,-1,-1,-1,0,127,6],
    "NUMEL":[3,1,0,127,24,0,255,0,128,255,6],
    "SHROOMISH":[2,1,0,127,0,0,127,24],
    "DELCATTY":[3,1,128,255,24,128,255,0,0,191,6],
    "VOLTORB":[3,1,0,127,12,128,255,12,128,255,0],
    "VULPIX":[3,1,128,255,18,0,127,6,128,255,0],
    "RALTS":[3,1,128,255,18,0,127,6,64,255,0],
    "MAWILE":[2,1,0,127,18,128,255,6],
    "SNORUNT":[1,1,0,127,6],
    "PINECO":[1,1,128,255,6],
    "NATU":[2,1,0,127,0,128,255,24],
    "ROSELIA":[2,1,128,255,18,128,255,6],
    "MEOWTH":[3,1,0,127,18,0,127,0,64,255,6],
    "SWINUB":[2,1,128,255,0,0,127,18],
    "SPEAROW":[2,1,0,127,6,128,255,18],
    "GRIMER":[2,1,128,255,18,128,255,12],
    "SEEL":[3,1,0,127,18,128,255,12,128,255,6],
    "LUNATONE":[2,1,128,255,18,0,127,0],
    "NOSEPASS":[3,1,0,127,12,128,255,18,128,255,0],
    "PARAS":[2,1,0,127,6,128,255,24],
    "PIDGEOTTO":[2,1,32,255,18,128,255,12],
    "TANGELA":[3,1,0,127,0,128,255,6,0,191,12],
    "MAGNETON":[3,1,0,127,12,128,255,0,0,255,18],
    "VENOMOTH":[3,1,128,255,12,0,255,24,0,127,18],
    "ARBOK":[4,1,0,127,18,0,127,12,0,127,0,128,255,6],
    "PRIMEAPE":[4,1,128,255,24,0,127,6,0,127,12,0,127,18],
    "GOLDUCK":[3,1,0,127,18,0,127,6,128,255,24],
    "DODRIO":[1,1,0,127,18],
    "POLIWRATH":[4,1,0,127,6,128,255,24,128,255,18,128,255,18],
    "DUGTRIO":[4,1,128,255,12,0,127,6,128,255,18,128,255,0],
    "MANECTRIC":[1,1,0,127,6],
    "DRAGONITE":[5,1,128,255,0,0,127,12,0,127,12,128,255,18,128,255,0],
    }
#=============================================================================================#
NATURES = {
    0:'HARDY',
    1:'LONELY',
    2:'BRAVE',
    3:'ADAMANT',
    4:'NAUGHTY',
    5:'BOLD',
    6:'DOCILE',
    7:'RELAXED',
    8:'IMPISH',
    9:'LAX',
    10:'TIMID',
    11:'HASTY',
    12:'SERIOUS',
    13:'JOLLY',
    14:'NAIVE',
    15:'MODEST',
    16:'MILD',
    17:'QUIET',
    18:'BASHFUL',
    19:'RASH',
    20:'CALM',
    21:'GENTLE',
    22:'SASSY',
    23:'CAREFUL',
    24:'QUIRKY',
    }
#=============================================================================================#
NATUREVERSE = {
    'HARDY':0,
    'LONELY':1,
    'BRAVE':2,
    'ADAMANT':3,
    'NAUGHTY':4,
    'BOLD':5,
    'DOCILE':6,
    'RELAXED':7,
    'IMPISH':8,
    'LAX':9,
    'TIMID':10,
    'HASTY':11,
    'SERIOUS':12,
    'JOLLY':13,
    'NAIVE':14,
    'MODEST':15,
    'MILD':16,
    'QUIET':17,
    'BASHFUL':18,
    'RASH':19,
    'CALM':20,
    'GENTLE':21,
    'SASSY':22,
    'CAREFUL':23,
    'QUIRKY':24,
    }
#=============================================================================================#
print('Pokemon XD: Gale of Darkness / Pokemon Colosseum Nature Lock Checker')
print('Version 2.1.1, written in Python 2.7.2')
print('Created by Zari/Zari01 (on Smogon and Reddit, respectively)')
print('Debugging/testing help provided by Smogon\'s CollectorTogami. Thanks man!\n')
#=============================================================================================#
go = True
while go == True:
    main()
    check = (raw_input('Done! All found data has been exported to .txt; Run another search? (y/n): ')).lower()
    if check != 'y':
        go = False
#=============================================================================================#
