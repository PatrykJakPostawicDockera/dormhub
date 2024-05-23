import { jwtDecode } from 'jwt-decode';

export interface JwtPayload {
  UserId: string;
  Nickname: string;
  RoomNumber: string;
  AvatarUrl: string;
  IsAdmin: boolean;
  DormId: string;
  Address: string;
  Name: string;
}

const decode = (token: string) => jwtDecode<JwtPayload>(token);

export default decode;
