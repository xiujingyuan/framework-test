from biztest.util.easymock.easymock import Easymock


class LongshangmiyangMock(Easymock):

    def update_grant_notice_success(self):
        api = "/report/kn/notice/callback"
        mode = '''{
          "code": 200,
          "message": "success",
          "datas": null
        }'''
        self.update(api, mode)


if __name__ == '__main__':
    longshang = LongshangmiyangMock('carltonliu', 'lx19891115', "5d43957a09acc30020bb1c69")
    longshang.update_grant_notice_success()
