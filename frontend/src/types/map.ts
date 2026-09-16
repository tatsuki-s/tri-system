interface Limit{
  front: number,
  back: number
}
interface Map{
  id: {
    id: number,
    name: string,
    branch: number | null,
    limit: Limit
    now_train: null | number
  }
}
export interface position{
  description: {
    id: string,
    name: string,
    loop: true | false
  },
  map: Map,
  branch: Map,
  settings: {
    defaultLimit: number
  }

}
