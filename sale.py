# -*- coding: utf-8 -*-
from openerp import tools
from openerp import models, fields, api,exceptions


class pres_sale(models.Model):
    _name = 'nantian_erp.pres_sale'

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
    nu = fields.Char(string='合同编号')
    bid_write = fields.Char(string='标书编写',)
    bid_checkman_id = fields.Many2one('res.users',string='标书复核人',)
    bid_readman_id = fields.Many2one('res.users',string='讲标人',)
    after_bid_amount = fields.Integer(string='合同/中标金额',)
    term = fields.Char(string='检索词',)
    firm_platform = fields.Char(string='涉及厂商或平台',)
    context = fields.Text(string='合同主要内容',)
    siger = fields.Many2one('res.users',string='签字人',)
    sign_date = fields.Date(string='签订日期',)

# 项目收款
class project_gathering(models.Model):#
    _name = 'nantian_erp.project_gathering'

    gather_progress= fields.Selection([('开始准备材料',u"开始准备材料"),
                             ('完成准备材料',u"完成准备材料"),
                             ('已提交审核',u"已提交审核"),
                             ('审核通过准备付款',u"审核通过准备付款"),
                             ('完成付款',u"完成付款"),
                             ],
                            string='调动人')
    # 准备收款材料时间前一周在周报该项中提醒需要开始准备收款，并给出此项工作进度选项：
    # 开始准备材料、完成准备材料、已提交审核、审核通过准备付款、完成付款。以此来反应收款工作进度。
    gather_date = fields.Date(string='收款日期')# 这个是Onetomany
    gather_reminder = fields.Char(string='特此提醒，开始准备收款！')




# 人员的调动
class pers_transfer(models.Model):#
    _name = 'nantian_erp.pers_transfer'

    name = fields.Char(string='调动人')
    res_contract_name = fields.Char(string='合同名称')
    res_contract_job = fields.Char(string='合同岗位')
    sour_team = fields.Char(string='原项目组')
    move_reason = fields.Char(string='调动原因')
    move_date = fields.Date(string='调动时间')
    is_recruit = fields.Boolean(string='是否招聘')
    after_leading = fields.Char(string='调动后负责人')
    befor_leading = fields.Char(string='调动后负责人')

    des_team = fields.Char(string='新项目组')
    des_contract_name = fields.Char(string='合同名称')
    des_contract_job = fields.Char(string='合同岗位')





# 人员的离职
class demission(models.Model):#
    _name = 'nantian_erp.demission'

    recruit_name = fields.Char(string='离职申请人')
    contract_name = fields.Char(string='合同名称')
    contract_post = fields.Char(string='合同岗位')
    sro_project = fields.Char(string='项目组')
    recruit_reason = fields.Char(string='离职原因')
    recruit_date = fields.Date(string='离职时间')
    is_recruit = fields.Boolean(string='是否招聘')




#  客户动态或人事变动
class customer_adjust(models.Model):
    _name = 'nantian_erp.customer_adjust'

    major_adjust = fields.Boolean(string='近一月客户是否有重大动态或人事变动')
    major_adjust_detail = fields.Char(string='详情叙述')



# 项目进度
class project_progress(models.Model):#
    _name = 'nantian_erp.project_progress'

    major_change = fields.Boolean(string='本周是否重大变更')
    major_change_detail = fields.Char(string='详情叙述')
    repeat = fields.Boolean(string='本周是否重保')
    repeat_detail = fields.Char(string='详情叙述')
    major_fault = fields.Boolean(string='本周是否重大事故')
    major_fault_detail = fields.Char(string='详情叙述')
    recruit_name = fields.Boolean(string='本周是否主机维护')
    recruit_name_detail = fields.Char(string='详情叙述')
    mantence = fields.Boolean(string='本周是否版本上线')
    mantence_detail = fields.Char(string='详情叙述')
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