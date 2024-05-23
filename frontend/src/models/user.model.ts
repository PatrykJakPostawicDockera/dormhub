export interface BaseUserModel {
  Name: string;
  Surname?: string;
  Nickname?: string;
  Nationality: number;
  Email: string;
  PhoneNumber: string;
  Birthday: string; // RRRR-MM-DD
  Gender: string;
  AboutMe: string;
  FacebookLink: string;
  InstagramLink: string;
  AvatarUrl: string;
}

export interface UserRegisterModel extends BaseUserModel {
  Password: string;
  DormCode: string;
  ArrivalDate: string; // RRRR-MM-DD
  DepartureDate: string; // RRRR-MM-DD
  IsAdmin: number;
  RoomNumber: string;
}

export interface UserDataModel extends BaseUserModel {
  UserId: string;
  DormId: string;
  RegistrationDate: string;
  ArrivalDate: string; // RRRR-MM-DD
  DepartureDate: string; // RRRR-MM-DD
  Age: number;
  IsAdmin: number;
  RoomNumber: string;
  ShowSurname: number;
  ShowAge: number;
  ShowDate: number;
  ShowEmail: number;
  ShowPhone: number;
  ShowSocial: number;
}
