export default interface PostModel {
  PostId: string;
  DormId: string;
  UserId: string;
  PostType: number;
  PostTitle: string;
  PostContent: string;
  Nickname: string;
  Date: string;
  Photos: string[];
}

export interface PostTypes {
  TypeId: number;
  Name: string;
}
