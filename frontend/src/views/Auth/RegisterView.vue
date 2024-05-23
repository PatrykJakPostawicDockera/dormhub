<template>
  <div class="flex min-h-screen w-screen justify-center p-20">
    <div class="flex flex-col gap-1">
      <p class="text-4xl font-medium text-textLight">
        Dorm<span class="font-bold text-primaryLight">Hub</span>
      </p>
      <p class="text-2xl">Register to start your journey in the dorm</p>
      <FormKit type="form" :actions="false" @submit="handleRegisterSubmit">
        <FormKit
          name="registration"
          type="multi-step"
          tab-style="progress"
          :hide-progress-labels="true"
        >
          <FormKit type="step" name="loginInfo">
            <FormKit
              name="suiteId"
              type="text"
              v-model="code"
              label="Suite code"
              placeholder="Suite code"
              validation="required"
            />
            <FormKit
              name="email"
              type="email"
              label="Email"
              placeholder="Email"
              validation="email|required"
            />
            <FormKit name="passGrp" type="group">
              <FormKit
                type="password"
                name="password"
                label="Password"
                help="Enter a new password"
                validation="required|length:6"
                validation-visibility="blur"
              />
              <FormKit
                type="password"
                name="password_confirm"
                label="Confirm password"
                help="Confirm your new password"
                validation="required|confirm"
                validation-visibility="blur"
                validation-label="Password confirmation"
              />
            </FormKit>
          </FormKit>
          <FormKit type="step" name="personalInfo">
            <FormKit
              name="name"
              type="text"
              label="Name"
              placeholder="Name"
              validation="required"
              validation-visibility="blur"
            />
            <FormKit name="surname" type="text" label="Surname (optional)" placeholder="Surname" />
            <FormKit
              name="nickname"
              type="text"
              label="Nickname (optional)"
              placeholder="Nickname"
            />
            <FormKit
              name="roomNumber"
              type="text"
              label="Room number"
              placeholder="Room number"
              validation="required"
              validation-visibility="blur"
            />
            <FormKit
              name="gender"
              type="select"
              label="Gender"
              :options="['Male', 'Female', 'Other', 'Prefer not to say']"
              validation="required"
              validation-visibility="dirty"
            />
            <FormKit
              name="birthday"
              type="date"
              label="Date of birth"
              placeholder="Date of birth"
              validation="required"
              validation-visibility="dirty"
            />
            <FormKit
              name="nationality"
              type="select"
              label="Nationality"
              :options="nationalities"
              validation="required"
              validation-visibility="dirty"
            />
          </FormKit>
          <FormKit type="step" name="aboutMe">
            <FormKit
              name="arrivalDate"
              type="date"
              label="Date of arrival"
              placeholder="Date of arrival"
              validation="required"
              validation-visibility="dirty"
            />
            <FormKit
              name="departureDate"
              type="date"
              label="Date of departure"
              placeholder="Date of departure"
              validation="required"
              validation-visibility="dirty"
            />
            <FormKit
              name="phoneNumber"
              type="text"
              label="Phone number (optional)"
              placeholder="Phone number"
              validation-visibility="dirty"
            />
            <div class="flex gap-5">
              <img
                alt="user avatar preview"
                id="preview"
                class="h-20 w-20 object-cover object-center"
                src=""
              />
              <FormKit
                name="profilePhoto"
                type="file"
                label="Avatar (optional)"
                placeholder="Avatar"
                validation-visibility="dirty"
                v-model="files"
              />
            </div>
            <FormKit
              name="aboutMe"
              type="textarea"
              label="About me (optional)"
              placeholder="Tell us something about yourself..."
            />
            <FormKit
              name="facebookLink"
              type="text"
              label="Facebook (optional)"
              placeholder="Link to Facebook profile"
              validation="url"
              validation-visibility="dirty"
            />
            <FormKit
              name="instagramLink"
              type="text"
              label="Instagram (optional)"
              placeholder="Link to Instagram profile"
              validation="url"
              validation-visibility="dirty"
            />
            <template #stepNext>
              <FormKit type="submit" />
            </template>
          </FormKit>
        </FormKit>
      </FormKit>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import type { UserRegisterModel } from '@/models/user.model';
import { useAuthStore } from '@/stores/auth';
import { fileToBase64 } from '@/helpers/imageToBase';
import type NationalityModel from '@/models/nationality.model';
import { apiInstance } from '@/helpers/api';

const props = defineProps<{
  suiteId?: string;
}>();

const code = ref('');
const nationalities = ref<Record<number, string>>({});
const files = ref<
  {
    name: string;
    file: File;
  }[]
>([]);

onMounted(async () => {
  code.value = props.suiteId ? props.suiteId : '';
  await apiInstance.get<NationalityModel[]>('nationalities').then((response) => {
    nationalities.value = response
      ? response.reduce(
          (acc, curr) => {
            acc[curr.NationalityId] = curr.Nationality;
            return acc;
          },
          {} as Record<number, string>,
        )
      : {};
  });
});

watch(files, (newFiles) => {
  const file = newFiles[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      const target = e.target as FileReader;
      const img = document.getElementById('preview') as HTMLImageElement;
      if (img) {
        img.src = target.result as string;
      }
    };
    reader.readAsDataURL(file.file);
  }
});

interface RegisterForm {
  registration: {
    loginInfo: {
      suiteId: string;
      email: string;
      passGrp: {
        password: string;
      };
    };
    personalInfo: {
      name: string;
      surname: string;
      nickname: string;
      roomNumber: string;
      gender: string;
      birthday: string;
      nationality: number;
    };
    aboutMe: {
      arrivalDate: string;
      departureDate: string;
      phoneNumber: string;
      profilePhoto: {
        name: string;
        file: File;
      }[];
      aboutMe: string;
      facebookLink: string;
      instagramLink: string;
    };
  };
}

const handleRegisterSubmit = async (fields: RegisterForm) => {
  const avatarUrl =
    fields.registration.aboutMe.profilePhoto.length > 0
      ? await apiInstance
          .post<{
            PhotoUrl: string;
          }>('inner/photos/upload', {
            PhotoData: await fileToBase64(fields.registration.aboutMe.profilePhoto[0].file),
          })
          .then((response) => {
            return response ? response.PhotoUrl : '';
          })
      : '';
  const dataField: UserRegisterModel = {
    DormCode: fields.registration.loginInfo.suiteId,
    Name: fields.registration.personalInfo.name,
    Surname: fields.registration.personalInfo.surname || '',
    Nickname: fields.registration.personalInfo.nickname || '',
    Nationality: fields.registration.personalInfo.nationality,
    Email: fields.registration.loginInfo.email,
    Password: fields.registration.loginInfo.passGrp.password,
    PhoneNumber: fields.registration.aboutMe.phoneNumber || '',
    Birthday: fields.registration.personalInfo.birthday,
    RoomNumber: fields.registration.personalInfo.roomNumber,
    Gender: fields.registration.personalInfo.gender,
    ArrivalDate: fields.registration.aboutMe.arrivalDate,
    DepartureDate: fields.registration.aboutMe.departureDate,
    AvatarUrl: avatarUrl,
    AboutMe: fields.registration.aboutMe.aboutMe || '',
    FacebookLink: fields.registration.aboutMe.facebookLink || '',
    InstagramLink: fields.registration.aboutMe.instagramLink || '',
    IsAdmin: 0,
  };

  await useAuthStore().register(dataField);
};
</script>
