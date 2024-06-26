import http from "@/api";
import { AnalysisPort } from "../config/servicePort";
import { EventAnalysis, ResDataList } from "../interface";

/** 根据日期获取卡片数据 */
export const getCardList = (date: string) => {
  return http.get<EventAnalysis.ResTopics>(AnalysisPort.MAIN.TOPICS, { date: date }, { loading: false });
};

/** 获取统计数据 */
export const getStatistics = (date: string) => {
  return http.get<EventAnalysis.ResStatistics>(AnalysisPort.MAIN.STATISTICS, { date: date }, { loading: false });
};

/** 获取折线表 */
export const getLineChart = (date: string) => {
  return http.get<EventAnalysis.ResLineChart>(AnalysisPort.MAIN.LINE_CHART, { date: date }, { loading: false });
};

/** 获取数据大屏的情感分析数据 */
export const getMainSentiment = (date: string) => {
  return http.get<ResDataList<EventAnalysis.ResEmotionAnalysis>>(AnalysisPort.MAIN.EMOTION, { date: date }, { loading: false });
};

export const getGraph3D = (date: string) => {
  return http.get<EventAnalysis.Res3DGraph>(AnalysisPort.MAIN.GRAPH3D, { date: date }, { loading: false });
};

export const getAllEvents = () => {
  return http.get<ResDataList<EventAnalysis.ResEvent>>(AnalysisPort.SEARCH, undefined, { loading: true });
};

/** 获取详细页面数据 */
export const getDetail = (title: string) => {
  return http.get<EventAnalysis.ResEventAnalysis>(AnalysisPort.DETAIL.EVENT, { title: title }, { loading: false });
};

/** 获取详细页面各个帖子的情感分析数据 */
export const getDetailedSentiment = (title: string) => {
  return http.get<ResDataList<EventAnalysis.ResDetailedSentiment>>(
    AnalysisPort.DETAIL.SENTIMENT,
    { title: title },
    { loading: false }
  );
};
