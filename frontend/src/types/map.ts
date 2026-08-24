//普通の線路，分岐，車止め
export type NodeType = 'block' | 'point' | 'buffer'

//本線方向，副本線方向
export type PointPosition = 'normal' | 'reverse'

//VueFlowでの描画用
export interface Position {
  x: number
  y: number
}

export interface MapNode {
  id: string
  type: NodeType
  name: string
  position: Position

  //通過可能速度
  speedLimit?: number
}

export interface Route {
  id: string

  //進行方向
  from: string
  to: string

  //副本線の場合，本線との合流地点までに通過するNode
  via?: string[]

  //このRouteを成立させるためのポイント状態
  point?: Record<string, PointPosition>

  //副本線の場合，分岐通過時の速度制限
  speedLimit?: number
}

export interface RailwayMap {
  version: number

  description: {
    id: string
    name: string
    unit?: string
  }

  nodes: MapNode[]
  routes: Route[]
}
