import { ATOStatus, ATSStatus, Direction, type TRICallFunctionData, type TRITrainFunctions, TRITrainTypes, TRIWebSocketDataType } from "./TRIEnumTypes"

export type TRIReceivedTrainData = {
    speed : number ,
    mc : number ,
    dir : Direction ,
    eb : boolean ,
    normal : boolean ,
    key : boolean, 
    asw : boolean ,
    courseChange : boolean
    course : number,
    trainType : TRITrainTypes,
    
    atc : boolean ,
    lim : number ,
    nextLim : number,
    forwardAlert : boolean,

    ato : boolean ,
    atoStat : ATOStatus ,

    ats : boolean ,
    atsStat : ATSStatus ,

    location:string,
    section:number,
    clientName:string,
    nextStop:boolean
}

export const TRIReceivedTrainDataDefault : TRIReceivedTrainData = {
    speed : 0 ,
    mc : 0 ,
    dir : Direction.stop ,
    eb :false ,
    normal : false ,
    key : true ,
    asw : false ,
    courseChange : true ,
    course : 0 ,
    trainType : TRITrainTypes.local,

    atc : false ,
    lim : 0 ,
    nextLim : 0,
    forwardAlert : true,

    ato : false ,
    atoStat : ATOStatus.beforeDeparture ,

    ats : false ,
    atsStat : ATSStatus.waiting,

    location:"M",
    section:0,
    clientName:"sample",
    nextStop : false
}

export type TRIWebSocketSingleJsonData = {
    key : string ,
    value : any
}

export type TRIWebSocketData = { 
    type : TRIWebSocketDataType.singleJson ,  
    main : TRIWebSocketSingleJsonData 
}|{
    type : TRIWebSocketDataType.callFunction,
    main : TRICallFunctionData
}|{
    type : TRIWebSocketDataType.trainStatus,
    main : TRIReceivedTrainData
}|{
    type : TRIWebSocketDataType.onChangeSection,
    main : string
}
    
