# -*- coding: utf-8 -*-
from openerp import tools
from openerp import models, fields, api,exceptions
import datetime


class weekly_reports(models.Model):
    _name = 'nantian_erp.weekly_reports'

    user_id = fields.Many2one('res.users',string='创建者',required=True,default=lambda self: self.env.user)#
    date = fields.Date(string='创建日期',default=lambda self:fields.datetime.now(),readonly = True)
    pres_sale_ids = fields.One2many('nantian_erp.pres_sale','weekly_reports_id',string='售前项目进展')
    gathering_ids = fields.One2many('nantian_erp.project_gathering','weekly_reports_id',string='项目收款')
    pers_transfer_ids = fields.One2many('nantian_erp.pers_transfer','weekly_reports_id',string='人员调动')
    demission_ids = fields.One2many('nantian_erp.demission','weekly_reports_id',string='人员离职')
    customer_adjust_ids = fields.One2many('nantian_erp.customer_adjust','weekly_reports_id',string='客户动态或人事变动')
    project_progress_ids = fields.One2many('nantian_erp.project_progress','weekly_reports_id',string='项目进度')

    test_field = fields.Char(string='测试字段')

    # 自动化动作每周创建一个周报，内容是cop上一周周报的所有内容
    @api.multi
    def create_weekly_reports(self):
        pass

    @api.multi
    @api.depends('date')
    def fetch_contract(self):
        now = fields.datetime.now()
        print "begin 触发动作", now
        print self.user_id.name
        objects = self.env['nantian_erp.contract'].search([("header_id", "=", self.user_id.id)])
        if objects:
            print "begin_找到了合同", objects
            for object in objects:
                if object.collection_ids:
                    print "begin_找到了收款合同", object.collection_ids
                    for collection in object.collection_ids:
                        if collection.materials_date:
                            print "begin_找到了材料的时间", collection.materials_date
                            SevenDayAgo = (now + datetime.timedelta(days=0))
                            ReminderDate = fields.Date.from_string(collection.materials_date)
                            print "七天后的时间", SevenDayAgo
                            print "准备材料的时间", ReminderDate
                            if SevenDayAgo == ReminderDate:
                                print "创建一个项目收款的表"
                                objects = self.env['nantian_erp.project_gathering'].create(
                                    {"contract_id": collection.contract_id.id, "gather_reminder": collection.name,
                                     "weekly_reports_id": self.id})

    # 自动化每天都检查本周里的项目收款是否到期
    # @api.multi
    # def fetch_contract(self):
    #     now = fields.datetime.now()
    #     print "begin 自动化动作",now
    #     for x in self:
    #         print
    #     print self.user_id.name
    #     objects = self.env['nantian_erp.contract'].search([("header_id", "=", self.user_id.id)])
    #     if objects:
    #         print "begin_找到了合同",objects
    #         for object in objects:
    #             if object.collection_ids:
    #                 print "begin_找到了收款合同", object.collection_ids
    #                 for collection in object.collection_ids:
    #                     if collection.materials_date:
    #                         print "begin_找到了材料的时间",collection.materials_date
    #                         SevenDayAgo = (now + datetime.timedelta(days=0))
    #                         ReminderDate= fields.Date.from_string(collection.materials_date)
    #                         print "七天后的时间",SevenDayAgo
    #                         print "准备材料的时间",ReminderDate
    #                         if SevenDayAgo == ReminderDate:
    #                             #创建一个项目收款的表
    #                             objects = self.env['nantian_erp.project_gathering'].create({"contract_id":collection.contract_id.id,"gather_reminder":collection.name,"weekly_reports_id":self.id})
    #


class pres_sale(models.Model):
    _name = 'nantian_erp.pres_sale'

    weekly_reports_id = fields.Many2one('nantian_erp.weekly_reports',string='周报')
    project_name = fields.Char(string='项目名称')
    contract_name = fields.Char(string='合同名称')
    partner = fields.Many2one('res.partner', string='客户名称', domain="[('category','=',u'服务客户')]")
    process_scrib = fields.Text(string='本周主要进展说明')
    before_bid_amount = fields.Integer(string='投标金额')
    bid_commpany = fields.Char(string='中标单位',)
    pre_bid_date = fields.Date(string='预计投标日期')
    competitors = fields.Char(string='竞争对手')
    rate_of_success = fields.Integer(string='预计成功率（%）')
    salesman_id = fields.Many2one('res.users', string='销售负责人')
    # 合同编号、项目名称、合同名称、客户名称、进展、
    # 标书编写、标书复核人、讲标人、投标金额、投标日期、中标单位、
    # 主要竞对、成功率、合同/中标金额、检索词、涉及厂商或平台、
    # 合同主要内容、销售人员、签字人、签订日
    # 项目名称、合同名称、进展、投标金额、投标日期、中标单位、主要竞对、成功率、
    contract_number = fields.Char(string='合同编号')
    bid_write = fields.Char(string='标书编写',)
    bid_checkman_id = fields.Many2one('res.users',string='标书复核人',)
    bid_readman_id = fields.Many2one('res.users',string='讲标人',)
    after_bid_amount = fields.Integer(string='合同/中标金额',)
    term = fields.Char(string='检索词',)
    firm_platform = fields.Char(string='涉及厂商或平台',)
    context = fields.Text(string='合同主要内容',)
    siger = fields.Many2one('res.users',string='签字人',)
    sign_date = fields.Date(string='签订日期',)
    state =fields.Selection(
        [
            (u'lose',u'未中标'),
            (u'win',u'项目开始'),
        ],string=u"状态")


    contract_view = {
        'name': ('创建合同'),
        'res_model': 'nantian_erp.contract',
        'views': [['form', False]],
        'type': 'ir.actions.act_window',
        #'target': 'new',
        'inherit_id':'nantian_erp_pres_sale_action',
        "domain": [[]],
    }


    def pop_window(self):
        return self.contract_view

    @api.multi
    def win_the_biding(self):
        self.state = 'win'
        return self.pop_window()

    @api.multi
    def lose_a_bid(self):
        self.state = 'lose'
        now1 = fields.datetime.now()
        # print now1.strptime('%j')
        # print now1.strptime
        print dir(now1)
        now2 = datetime.datetime.now()
        # hyhh
        print dir(now2)

        return {'aa'}

# 项目收款
class project_gathering(models.Model):#
    _name = 'nantian_erp.project_gathering'

    weekly_reports_id = fields.Many2one('nantian_erp.weekly_reports', string='周报')
    contract_id = fields.Many2one('nantian_erp.contract', string='合同')
    gather_date = fields.Date(string='！')
    gather_progress= fields.Selection([('开始准备材料',u"开始准备材料"),
                             ('完成准备材料',u"完成准备材料"),
                             ('已提交审核',u"已提交审核"),
                             ('审核通过准备付款',u"审核通过准备付款"),
                             ('完成付款',u"完成付款"),
                             ],
                            string='收款工作进度')
    # 准备收款材料时间前一周在周报该项中提醒需要开始准备收款，并给出此项工作进度选项：
    # 开始准备材料、完成准备材料、已提交审核、审核通过准备付款、完成付款。以此来反应收款工作进度。
    # gather_date = fields.Date(string='收款日期')
    collection_ids = fields.One2many('nantian_erp.collection','project_gathering_id',string='合同收款表')
    gather_reminder = fields.Char(string='特此提醒，开始准备收款！')
    # 这个字段填写的是到哪一期第几阶段




    # 自动化每天都检查本周里的项目收款是否到期
    # @api.multi
    # def fetch_contract(self):


# 人员的调动
class pers_transfer(models.Model):#
    _name = 'nantian_erp.pers_transfer'

    weekly_reports_id = fields.Many2one('nantian_erp.weekly_reports', string='周报')
    name = fields.Many2one('res.users',string='调动人')
    res_contract_name = fields.Char(string='合同名称')
    res_contract_job = fields.Char(string='合同岗位')
    sour_team = fields.Char(string='原项目组')
    move_reason = fields.Char(string='调动原因')
    move_date = fields.Date(string='调动时间')
    is_recruit = fields.Boolean(string='是否招聘')
    after_leading = fields.Many2one('res.users',string='调动后负责人')
    before_leading = fields.Many2one('res.users',string='调动后负责人')

    des_team = fields.Char(string='新项目组')
    des_contract_name = fields.Char(string='合同名称')
    des_contract_job = fields.Char(string='合同岗位')



# 人员的离职
class demission(models.Model):#
    _name = 'nantian_erp.demission'

    weekly_reports_id = fields.Many2one('nantian_erp.weekly_reports', string='周报')
    recruit_name = fields.Many2one('res.users',string='离职申请人')
    contract_name = fields.Char(string='合同名称')
    contract_post = fields.Char(string='合同岗位')
    sro_project = fields.Char(string='项目组')
    recruit_reason = fields.Char(string='离职原因')
    recruit_date = fields.Date(string='离职时间')
    is_recruit = fields.Boolean(string='是否招聘')




#  客户动态或人事变动
class customer_adjust(models.Model):
    _name = 'nantian_erp.customer_adjust'

    weekly_reports_id = fields.Many2one('nantian_erp.weekly_reports', string='周报')
    major_adjust = fields.Boolean(string='近一月客户是否有重大动态或人事变动')
    major_adjust_detail = fields.Char(string='详情叙述')



# 项目进度
class project_progress(models.Model):
    _name = 'nantian_erp.project_progress'

    weekly_reports_id = fields.Many2one('nantian_erp.weekly_reports', string='周报')
    major_change = fields.Boolean(string='本周是否重大变更')
    major_change_detail = fields.Char(string='详情叙述')
    repeat = fields.Boolean(string='本周是否重保')
    repeat_detail = fields.Char(string='详情叙述')
    major_fault = fields.Boolean(string='本周是否重大事故')
    major_fault_detail = fields.Char(string='详情叙述')
    maintenance = fields.Boolean(string='本周是否主机维护')
    maintenance_detail = fields.Char(string='详情叙述')
    ver_on_line = fields.Boolean(string='本周是否版本上线')
    ver_on_line_detail = fields.Char(string='详情叙述')
    equipment_implementation = fields.Boolean(string='本周是否设备实施')
    equipment_implementation_detail = fields.Char(string='详情叙述')
    special = fields.Boolean(string='本周是否有特殊事项')
    special_detail = fields.Char(string='详情叙述')
    possible_risk = fields.Boolean(string='本周预计可能风险')
    possible_risk_detail = fields.Char(string='详情叙述')
    # 项目进度方面分为几个类型问题：
    # 本周是否重大变更、本周是否重保、
    # 本周是否重大事故、本周是否主机维护、
    # 本周是否版本上线、本周是否设备实施、
    # 本周是否有特殊事项、本周预计可能风险，
    # 如选是，则详细描述（或设置更详细问题）


# class excel_transfer(models.Model):#
#     _name = 'nantian_erp.excel_transfer'
#
#     name = fields.Char(string='姓名')
#     oa_number = fields.Char(string='OA账号')
#     transfer_type = fields.Selection([
#             (u'人员离职', u"人员离职"),
#             (u'人员调动', u"人员调动"),
#                                      ],string='部门调整类型',)
#     transfer_instruction = fields.Integer(string='部门调整说明')
#     # 原属部门
#     one_department = fields.Char(string='一级部门')
#     two_department = fields.Char(string='二级部门')
#     three_department = fields.Char(string='三级部门')
#     four_department = fields.Char(string='四级部门')
#     # 新属部门
#     new_one_department = fields.Char(string='一级部门')
#     one_department_leader = fields.Char(string='一级部门审批负责人')
#     new_two_department = fields.Char(string='二级部门')
#     two_department_leader = fields.Char(string='二级部门审批负责人')
#     new_three_department = fields.Char(string='三级部门')
#     three_department_leader = fields.Char(string='三级部门审批负责人')
#     new_four_department = fields.Char(string='四级部门')
#     four_department_leader = fields.Char(string='四级部门审批负责人')
#
#     new_part_number = fields.Char(string='新末级部门编号')