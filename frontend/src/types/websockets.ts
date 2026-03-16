export interface Camera {
  type: "camera",
  main: {
    trainId: number,
    readId: number
  }
}
export type WSMessage = Camera
