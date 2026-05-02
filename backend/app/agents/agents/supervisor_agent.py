"""
监督代理 - 使用LangGraph自带supervisor
负责协调各个专门代理的工作流程
pip install langgraph-supervisor
"""
from typing import Dict, Any, List

from langchain_core.runnables import RunnableConfig
from langgraph_supervisor import create_supervisor

from app.core.state import SQLMessageState
from app.core.llms import get_default_model
# fmt: off  MC80OmFIVnBZMlhucUx2b2pZbmt1cm82VUdGU2JnPT06M2M3ZjdiOTI=


class SupervisorAgent:
    """监督代理 - 基于LangGraph自带supervisor"""

    def __init__(self, worker_agents: List[Any] = None):
        self.llm = get_default_model()
        self.worker_agents = worker_agents or self._create_worker_agents()
        self.supervisor = self._create_supervisor()

    def _create_worker_agents(self) -> List[Any]:
        """创建工作代理"""
        from app.agents.agents.schema_agent import schema_agent
        from app.agents.agents.sample_retrieval_agent import sample_retrieval_agent
        from app.agents.agents.sql_generator_agent import sql_generator_agent
        from app.agents.agents.sql_validator_agent import sql_validator_agent
        from app.agents.agents.sql_executor_agent import sql_executor_agent
        from app.agents.agents.error_recovery_agent import error_recovery_agent
        from app.agents.agents.chart_generator_agent import chart_generator_agent
# pragma: no cover  MS80OmFIVnBZMlhucUx2b2pZbmt1cm82VUdGU2JnPT06M2M3ZjdiOTI=

        # 返回agent对象而不是包装类
        return [
            schema_agent.agent,
            # sample_retrieval_agent.agent,
            sql_generator_agent.agent,
            sql_validator_agent.agent,
            # parallel_sql_validator_agent.agent,
            sql_executor_agent.agent,
            error_recovery_agent.agent,
            chart_generator_agent.agent
        ]

    # def pre_model_hook(self, state):
    #     print("哈哈哈哈哈：：：：", state)
    def _create_supervisor(self):
        """创建LangGraph supervisor"""
        supervisor = create_supervisor(
            model=self.llm,
            agents=self.worker_agents,
            prompt=self._get_supervisor_prompt(),
            add_handoff_back_messages=True,
            # pre_model_hook=self.pre_model_hook,
            # parallel_tool_calls=True,
            output_mode="full_history",
        )

        return supervisor.compile()

    # 📚 ** sample_retrieval_agent **: 检索相关的SQL问答对样本，提供高质量参考
    # sample_retrieval_agent →

    # ** 样本检索优化: **
    # - 基于用户查询语义检索相似问答对
    # - 结合数据库结构进行结构化匹配
    # - 提供高质量SQL生成参考样本
    def _get_supervisor_prompt(self) -> str:
        """获取监督代理提示"""
        # print("=== 提取连接ID ===")
        # print(f"状态类型: {type(state)}")
        # print(state)
        # # 从消息中提取连接ID
        # connection_id = None  # 默认值
        # messages = state.get("messages", []) if isinstance(state, dict) else getattr(state, "messages", [])
        #
        # for message in reversed(messages):
        #     if hasattr(message, 'type') and message.type == 'human':
        #         if hasattr(message, 'additional_kwargs') and message.additional_kwargs:
        #             msg_connection_id = message.additional_kwargs.get('connection_id')
        #             if msg_connection_id:
        #                 connection_id = msg_connection_id
        #                 print(f"从消息中提取到连接ID: {connection_id}")
        #                 break
        #
        # # 更新state中的connection_id，确保所有后续agents都能获取到正确的连接ID
        # if isinstance(state, dict):
        #     state['connection_id'] = connection_id
        # else:
        #     state.connection_id = connection_id
        #
        # print(f"最终使用连接ID: {connection_id}")
        # print(f"已更新state.connection_id = {connection_id}")
        # print("==================")
# type: ignore  Mi80OmFIVnBZMlhucUx2b2pZbmt1cm82VUdGU2JnPT06M2M3ZjdiOTI=

        system_msg = f"""你是一个智能的SQL Agent系统监督者。
你管理以下专门代理：

🔍 **schema_agent**: 分析用户查询，获取相关数据库表结构

⚙️ **sql_generator_agent**: 根据模式信息和样本生成高质量SQL语句
🔍 **sql_validator_agent**: 验证SQL的语法、安全性和性能
🚀 **sql_executor_agent**: 安全执行SQL并返回结果
📊 **chart_generator_agent**: 根据查询结果生成数据可视化图表
🔧 **error_recovery_agent**: 处理错误并提供修复方案

**工作原则:**
1. 根据当前任务阶段选择合适的代理
2. 确保工作流程的连续性和一致性
3. 智能处理错误和异常情况
4. 一次只分配给一个代理，不要并行调用
5. 不要自己执行任何具体工作

**标准流程:**
用户查询 → schema_agent → sql_generator_agent → sql_validator_agent → sql_executor_agent → [可选] chart_generator_agent → 完成

**图表生成条件:**
- 用户查询包含可视化意图（如"图表"、"趋势"、"分布"、"比较"等关键词）
- 查询结果包含数值数据且适合可视化
- 数据量适中（2-1000行）


**错误处理:**
任何阶段出错 → error_recovery_agent → 重试相应阶段

请根据当前状态和任务需求做出最佳的代理选择决策。特别注意：
- 当用户查询包含可视化意图时，在SQL执行完成后应考虑调用chart_generator_agent
- 当查询结果适合可视化时，主动建议生成图表"""

        return system_msg

    async def supervise(self, state: SQLMessageState) -> Dict[str, Any]:
        """监督整个流程"""
        try:
            result = await self.supervisor.ainvoke(state)
            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
# pylint: disable  My80OmFIVnBZMlhucUx2b2pZbmt1cm82VUdGU2JnPT06M2M3ZjdiOTI=


def create_supervisor_agent(worker_agents: List[Any] = None) -> SupervisorAgent:
    """创建监督代理实例"""
    return SupervisorAgent(worker_agents)

def create_intelligent_sql_supervisor() -> SupervisorAgent:
    """创建智能SQL监督代理的便捷函数"""
    return SupervisorAgent()
