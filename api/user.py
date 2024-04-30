import json
import sys
from functools import wraps
from fake_useragent import UserAgent
import requests


def auth_require(func):
    @wraps(func)
    def decorate(self, *args, **kwargs):
        if not self._authed:
            raise ValueError("Вы не авторизованы!")
        return func(self, *args, **kwargs)

    return decorate


class User:
    def __init__(self, login: str = None, password: str = None,
                 ):
        self.login, self.password = login, password
        self._authed = False
        self.session = requests.Session()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['session']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.session = requests.Session()
        if self._authed:
            self.auth()

    def auth(self, login: str = None, password: str = None):
        if login is None:
            login = self.login
        else:
            self.login = login

        if password is None:
            password = self.password
        else:
            self.password = password

        auth = self.session.post('https://passport.yandex.ru/passport?mode=auth',
                                 headers={'user-agent': UserAgent().random},
                                 data={'login': login, 'passwd': password})
        if auth.url == 'https://passport.yandex.ru/profile':
            self._authed = True
            return self
        else:
            self._authed = False
            if 'Неправильный' in auth.text:
                raise ValueError('Неправильные логин или пароль')
            raise ValueError('Ошибка X')

    @auth_require
    def get_lesson_ids(self, course_id: int, group_id: int):
        url = 'https://lyceum.yandex.ru/api/student/lessons'
        lessons = self.session.get(url, params={'groupId': group_id, 'courseId': course_id}).json()
        lesson_ids = list(lesson['id'] for lesson in lessons)
        return lesson_ids

    @auth_require
    def get_all_tasks(self, lesson_id: int, course_id: int):
        url = 'https://lyceum.yandex.ru/api/student/lessonTasks'
        lesson_info = self.session.get(url, params={'courseId': course_id, 'lessonId': lesson_id}).json()
        return lesson_info

    @auth_require
    def get_task(self, task_id: int, group_id: int):
        url = f'https://lyceum.yandex.ru/api/student/tasks/{task_id}'
        task = self.session.get(url, params={'groupId': group_id}).json()
        return task

    @auth_require
    def get_lesson_info(self, lesson_id: int, group_id: int, course_id: int):
        url = f'https://lyceum.yandex.ru/api/student/lessons/{lesson_id}'
        lesson_info = self.session.get(url, params={'groupId': group_id, 'courseId': course_id}).json()
        return lesson_info

    @auth_require
    def get_courses_groups_ids(self):
        url = r'https://lyceum.yandex.ru/api/profile'
        courses = self.session.get(url=url, params={'onlyActiveCourses': True,
                                                    'withCoursesSummary': True,
                                                    'withExpelled': True}).json()
        courses = courses['coursesSummary']['student']
        ids = [{'title': course['title'],
                'rating': course['rating'],
                'course_id': course['id'],
                'group_id': course['group']['id']}
               for course in courses]
        return ids

    @auth_require
    def get_course(self, with_rating: bool = False):
        courses = self.get_courses_groups_ids()
        if courses:
            print("Выберите курс:")
            print(*(f"  {course['title']} - {n}" for n, course in enumerate(courses)), sep='\n')
            n = input()
            while not (n.isdigit() and -1 < int(n) < len(courses)):
                print("Ошибка! Введите число от 0 до", len(courses) - 1, file=sys.stderr)
                n = input()
            print('===========\n')
            course = courses[int(n)]
            if with_rating:
                return course['course_id'], course['group_id'], course['rating']
            else:
                return course['course_id'], course['group_id']
        else:
            raise ValueError("У Вас нет курсов")
