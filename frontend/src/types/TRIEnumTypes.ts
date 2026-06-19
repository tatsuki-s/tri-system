export const enum Direction {
    stop = 0 ,
    forward = 1 ,
    backward = -1
}

export const enum ATOStatus {
    beforeDeparture = 0 ,
    driving = 1 ,
    pause = 2 ,
    arrived = 3
}

export const enum ATSStatus {
    waiting = 0 ,
    onAlert = 1 ,
    checked = 2 
}

export const enum TRIWebSocketDataType {
    singleJson = "singleJson" ,
    trainStatus = "trainStatus" ,
    callFunction = "callFunction",
    onChangeSection = "onChangeSection"
}

export const enum TRIAtcSignal {
    R=0,
    YY=1,
    Y=2,
    GY=3,
    G=4
}

export type TRISingleJsonData = {
    key : TRISingleJsonKey ,
    value : any
}

export const enum TRITrainTypes {
    local = 0,
    rapid = 1,
    express = 2
}

export type TRICallFunctionData = {
    name:TRITrainFunctions,
    args:object
}

export type TRISingleJsonKey="RTCLimSpeed"|"ats"|"ato"|"atc"|"atcSignal"|"operation_stop"|"asw"|"backwardSection"|"forwardSection"|"backwardLimit"|"forwardLimit"|"location"|"section"|"trainType";
export type TRITrainFunctions = "TriggerATS"|"choiceNextLimit"

export type LocationStr = "A"|"B"|"C"|"D"|"E"|"F"|"G"|"H"|"I"|"J"|"K"|"L"|"M"|"N"|"O"|"P"|"Q"|"R"|"S"|"T"|"U"|"V"|"W"|"X"|"Y"|"Z"

export type Digit = "0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9";
export type Sections = `${Digit}` | `${Digit}${Digit}`;
export type Positions = `${LocationStr}${Sections}`;