export interface Camera {
  type: "camera",
  main: {
    id: number,
    status: string,
    read_id: number
  }
}
export type WSMessage = Camera
