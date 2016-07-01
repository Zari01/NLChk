#===================================================================================#
def infograbber():
    usrtarget = raw_input('Enter Target PKMN name: ')
    usrtarget = usrtarget.upper()
    try:
        pkmn = POKEMON[usrtarget]
    except KeyError:
        print('Entered pokemon not found in database; program restarting.\n')
        infograbber()
    try:
        usrseed = int('0x' + raw_input("Enter Hexadecimal IV frame 1 Seed: 0x"), 16)
        if usrseed > 0xFFFFFFFF:
            raise ValueError
    except ValueError:
        print('Entered seed is invalid and cannot be used; program restarting.\n')
        infograbber()
    final_result = casehandler(usrseed,usrtarget,pkmn)
    print(final_result + '\n')
    hseed = hexify(usrseed)
    if final_result[0:1] == 'H':
        var_name = "NLChk_Valid"
    else:
        var_name = "NLChk_Invalid"
    var_name = var_name + ".txt"
    string = hseed + ', ' + final_result
    outputtotxt(var_name,string)
    print('Entered pokemon, seed, and subsequent result have been exported to .txt.\n')
    infograbber()

#===================================================================================#

def casehandler(seed,target_name,target_db):
    name = target_name
    nlnum = target_db[0]
    pkmnpos = target_db[1]
    if nlnum == 0:
        frv_str = RESULT[0] + name + REASON[0]
        return frv_str
    elif nlnum == 1:
        if pkmnpos == 1:
            pf_str,r_str = sNL_1S(seed,target_db)
            frv_str = pf_str + name + r_str
            return frv_str
        else:
            pf_str,r_str = sNL_2S(seed,target_db)
            frv_str = pf_str + name + r_str
            return frv_str
    else:
        if pkmnpos == 1:
            pf_str,r_str = mNL_1S(seed,target_db)
            frv_str = pf_str + name + r_str
            return frv_str
        else:
            pf_str,r_str = mNL_2S(seed,target_db)
            frv_str = pf_str + name + r_str
            return frv_str

#===================================================================================#

def sNL_1S(seed,pkmn):
    s = prngbackward(seed,1)
    gv,nl,s = gvnlchkB(s)
    test = gvcomp(gv,pkmn[2],pkmn[3])
    if test == True and nl == pkmn[4]:
        pfstring = RESULT[0]
        rstring = REASON[1]
        return pfstring,rstring
    else:
        pfstring = RESULT[1]
        rstring = REASON[3]
        return pfstring,rstring

#===================================================================================#

def sNL_2S(seed,pkmn):
    j,s = sstest(pkmn,seed)
    if j == -1:
        pfstring = RESULT[1]
        rstring = REASON[5]
        return pfstring,rstring
    else:
        pfstring = RESULT[0]
        rstring = REASON[2]+SETUP[j]
        return pfstring,rstring

#===================================================================================#

def mNL_1S(seed,pkmn):
    timesB = []
    timesF = []
    for v in range(0,pkmn[0],1):
        n = (v * 3) + 4
        nltest = pkmn[n]
        gvmin = pkmn[n-2]
        gvmax = pkmn[n-1]
        if v == 0:
            s = prngbackward(seed,1)
            gv,nl,s = gvnlchkB(s)
            test = gvcomp(gv,pkmn[2],pkmn[3])
            if (test == True and nl == pkmn[4]):
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
    for x in range(pkmn[0],0,-1):
        n = (x * 3) + 1
        nltest = pkmn[n]
        gvmin = pkmn[n-2]
        gvmax = pkmn[n-1]
        if x == pkmn[0]:
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

#===================================================================================#

def mNL_2S(seed,pkmn):
    timesB = []
    timesF = []
    for z in range(0,pkmn[0],1):
        n = (z*3)+4
        nltest = pkmn[n]
        gvmin = pkmn[n-2]
        gvmax = pkmn[n-1]
        if z == 0:
            j,s = sstest(pkmn,seed)
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
    for k in range(pkmn[0],0,-1):
        n = (k*3)+1
        nltest = pkmn[n]
        gvmin = pkmn[n-2]
        gvmax = pkmn[n-1]
        if k == pkmn[0]:
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

#===================================================================================#

def sstest(pkmn,usrseed):
    s = prngbackward(usrseed,6)
    for j in range(3):
        gv,nl,s = gvnlchkB(s)
        test = gvcomp(gv,pkmn[2],pkmn[3])
        if(test == True and nl == pkmn[4]):
            return (j,s)
    return (-1,s)

#===================================================================================#


def gvnlchkB(seed):
    s = prngbackward(seed,1)
    pidl = s >> 16
    s = prngbackward(s,1)
    pidh = s >> 16
    pid = (pidh << 16) + pidl
    gv = pid & 0xFF
    nl = pid % 25
    return (gv,nl,s)

#===================================================================================#

def gvnlchkF(seed):
    s = prngforward(seed,1)
    pidh = s >> 16
    s = prngforward(s,1)
    pidl = s >> 16
    pid = (pidh << 16) + pidl
    gv = pid & 0xFF
    nl = pid % 25
    return (gv,nl,s)

#===================================================================================#

def gvcomp(gvval,gvmin,gvmax):
    if(gvval >= gvmin and gvval <= gvmax):
        return True
    return False

#===================================================================================#

def hexify(seed):
    hseed = hex(seed)
    hseed = hseed[2:]
    while len(hseed) < 8:
        hseed = '0' + hseed
    hseed = '0x' + hseed
    return hseed

#===================================================================================#

def prngbackward(seed, times):
    s = seed
    for i in range(times):
        s = (s * 0xB9B33155 + 0xA170F641) & 0xFFFFFFFF
    return s

#===================================================================================#

def prngforward(seed, times):
    s = seed
    for q in range(times):
        s = (s * 0x000343FD + 0x00269EC3) & 0xFFFFFFFF
    return s

#===================================================================================#

def outputtotxt(txtname,string):
    txtf = open(txtname, 'a')
    txtf.write(string + '\n')
    txtf.close()

#===================================================================================#

SETUP = {
    0:'first shadow pokemon IVs/Nature set.',
    1:'first shadow pokemon IVs/Nature unset.',
    2:'first shadow pokemon IVs/Nature unset + shiny PID reroll.'
    }

#===================================================================================#

RESULT = {
    0:'Hypothetically valid IV/Nature combo for ',
    1:'Invalid IV/Nature combo for '
    }

#===================================================================================#

REASON = {
    0:'; this pokemon has no NLs!',
    1:'; passes NL(s).',
    2:'; passes NL(s) with ',
    3:'; fails NL closest to target.',
    4:'; NLs will always result in earlier frame(s) than the intended target.',
    5:'; fails all possible 1st shadow combos for the closest NL.'
    }

#===================================================================================#

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
#===================================================================================#
print('Pokemon XD: Gale of Darkness / Pokemon Colosseum Nature Lock Checker')
print('Version 1.4.0, written in Python 2.7.2')
print('Created by Zari/Zari01 (on Smogon and Reddit, respectively)')
print('Debugging/testing help provided by Smogon\'s CollectorTogami. Thanks man!\n')
infograbber()
