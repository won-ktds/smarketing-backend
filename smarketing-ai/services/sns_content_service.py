"""
SNS 콘텐츠 생성 서비스 (플랫폼 특화 개선)
"""
import os
from typing import Dict, Any, List, Tuple
from datetime import datetime
from utils.ai_client import AIClient
from utils.image_processor import ImageProcessor
from models.request_models import SnsContentGetRequest


class SnsContentService:

    def __init__(self):
        """서비스 초기화"""
        self.ai_client = AIClient()
        self.image_processor = ImageProcessor()

        # 블로그 글 예시
        self.blog_example = [
            {
                "raw_html": """<div class="se-main-container">
                    <div class="se-component se-text se-l-default" id="SE-80d4c6a7-4a37-11f0-b773-29c6aad03a11">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-f274648e-a47d-4112-85ee-088f2b77ed2c"><span style="" class="se-fs-fs28 se-ff-nanummyeongjo   " id="SE-9d63696b-4a37-11f0-b773-73be93bb9775"><b>팔공</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-a27a40de-cd51-4602-9d76-49f3527cd816"><span style="" class="se-fs-fs13 se-ff-nanumbarungothic   " id="SE-9d63696c-4a37-11f0-b773-f16c58bc9dec">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-32a904d2-f58d-4531-85c1-5456475f050b"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63696d-4a37-11f0-b773-75537d6268a5">중국음식하면 짬뽕이 제일 먼저 저는 떠오릅니다. 어릴 적 부터 짜장은 그닥 좋아하지 않았기에 지금도 짜장 보다는 짬뽕 그리고 볶음밥을 더 사랑합니다.(탕수육도 그닥 좋아하지는 않습니다) 지난 주말 11시30분쯤 갔다가 기겁(?)을 하고 일산으로 갔었던 기억이 납니다. 이날은 평일 조금 늦은 시간이기에 웨이팅이 없겠지 하고 갔습니다. 다행히 웨이팅은 없는데 홀에 딱 한자리가 있어서 다행히 착석을 하고 주문을 합니다.</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-80d4c6a7-4a37-11f0-b773-29c6aad03a11&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-image se-l-default __se-component" id="SE-8ce82d8d-3e55-481e-bff5-93e5417b14d4">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-8ce82d8d-3e55-481e-bff5-93e5417b14d4&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTFfODAg/MDAxNzQ5NjM3MzQ2NDM0.0_aheJqXCEDtEMgWPeLkNKwhoCg72NlXWMTEro0LyGIg.xWKBNIuvbxVNBhMYZdvFyGdc3Vx9gUVm8oA61VYVlcog.JPEG/20250611_140605.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTFfODAg/MDAxNzQ5NjM3MzQ2NDM0.0_aheJqXCEDtEMgWPeLkNKwhoCg72NlXWMTEro0LyGIg.xWKBNIuvbxVNBhMYZdvFyGdc3Vx9gUVm8oA61VYVlcog.JPEG/20250611_140605.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-8ce82d8d-3e55-481e-bff5-93e5417b14d4_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-8ce82d8d-3e55-481e-bff5-93e5417b14d4&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="se-component se-quotation se-l-quotation_line" id="SE-9345c9d1-81e1-41e4-bef2-9ae0f1d14d5c">
                        <div class="se-component-content">
                            <div class="se-section se-section-quotation se-l-quotation_line">
                                <blockquote class="se-quotation-container">
                                    <div class="se-module se-module-text se-quote"><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-9782c2c3-664d-49eb-a7d5-3b90f718c732"><span style="color:#1808f9;" class="se-fs-fs24 se-ff-   " id="SE-9d63696e-4a37-11f0-b773-bfb30c3d1899"><b>중화요리 팔공</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-81b3f607-02bc-413d-a30c-7afac66aaa4b"><span style="" class="se-fs-fs15 se-ff-   " id="SE-9d63696f-4a37-11f0-b773-b3a4f08d5316">위치안내: </span><span style="color:#000000;" class="se-fs-fs15 se-ff-  se-style-unset " id="SE-9d636970-4a37-11f0-b773-a37f5627147a">서울 관악구 남부순환로 1680</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-657363e0-d57c-4431-b965-09df1ffb5a3e"><span style="" class="se-fs-fs15 se-ff-   " id="SE-9d636971-4a37-11f0-b773-935bc83dbc74">영업시간: 11시 20분 ~ 21시 30분( 15시 ~ 17시 브레이크타임, 일요일 휴무)</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-e19b49c9-ae18-4fd9-95e4-2c3d14d1cfee"><span style="" class="se-fs-fs15 se-ff-   " id="SE-9d636972-4a37-11f0-b773-dd693147aaf0">메뉴: 짜장면, 해물짬뽕, 고기짬뽕, 볶음밥, 탕수육등</span></p><!-- } SE-TEXT --></div>
                                </blockquote>
                            </div>
                        </div>
                    </div>
                    <div class="se-component se-quotation se-l-quotation_line" id="SE-a2aa20bf-ab9a-49d0-895c-c9079ffc29db">
                        <div class="se-component-content">
                            <div class="se-section se-section-quotation se-l-quotation_line">
                                <blockquote class="se-quotation-container">
                                    <div class="se-module se-module-text se-quote"><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-1834d17e-3525-40e4-9bec-2c8dbda20834"><span style="color:#1808f9;" class="se-fs- se-ff-   " id="SE-9d636973-4a37-11f0-b773-f9895d05b192"><b>3명이 주문한 메뉴는 짜장면, 옛날볶음밥, 팔공해물짬뽕 2개 총 4가지 주문을 합니다.</b></span></p><!-- } SE-TEXT --></div>
                                </blockquote>
                            </div>
                        </div>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-a1368821-e6e2-4960-9c3b-1a74edae3ced">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-7d438d7f-a578-4b50-a873-87035aebbdcd"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d636974-4a37-11f0-b773-5b96c9a9b3b0">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-a1368821-e6e2-4960-9c3b-1a74edae3ced&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-placesMap se-l-default __se-component" id="SE-c2000acc-2f91-4e07-8259-9963e40aae73">
                        <div class="se-component-content">
                            <div class="se-section se-section-placesMap  se-section-align- se-l-default">
                                <div class="se-module se-module-map-image" style="padding-top: 45%;"><div class="__se_map se-dynamic-map" tabindex="0" style="position: relative; overflow: hidden; background: rgb(248, 249, 250);"><div style="position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; overflow: visible; width: 100%; height: 100%; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); z-index: 0; cursor: url(&quot;https://ssl.pstatic.net/static/maps/mantle/2x/openhand.cur&quot;), default;"><div style="position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; overflow: visible; width: 100%; height: 100%; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); z-index: 0;"><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 1;"><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: none; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 0; user-select: none;"></div><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 1; user-select: none;"><div style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 0px; height: 0px; overflow: visible; box-sizing: content-box !important;"><div draggable="false" unselectable="on" style="position: absolute; top: -33px; left: 250px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111752/50795@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 223px; left: 250px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111752/50796@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -289px; left: 250px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111752/50794@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -289px; left: 506px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111753/50794@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 223px; left: -6px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111751/50796@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -33px; left: 506px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111753/50795@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -33px; left: -6px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111751/50795@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 223px; left: 506px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111753/50796@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -289px; left: -6px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111751/50794@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -289px; left: 762px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111754/50794@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 223px; left: -262px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111750/50796@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -33px; left: 762px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111754/50795@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -33px; left: -262px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111750/50795@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 223px; left: 762px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111754/50796@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -289px; left: -262px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111750/50794@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div></div></div><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 100;"><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 101;"></div><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 103;"><div title="" style="position: absolute; overflow: hidden; box-sizing: content-box !important; cursor: inherit; left: 337px; top: 119px; width: 32px; height: 42px;"><img draggable="false" unselectable="on" src="https://editor-static.pstatic.net/c/resources/common/img/common-icon-places-marker-x2-20180920.png" alt="" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; position: absolute; cursor: pointer; width: 32px; height: 42px; left: 0px; top: 0px;"></div></div><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 106;"></div></div></div><div style="position: absolute; display: none; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; overflow: visible; width: 100%; height: 100%; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); background-color: rgb(255, 255, 255); z-index: 10000; opacity: 0.5;"></div></div></div><div style="position: absolute; z-index: 100; margin: 0px; padding: 0px; pointer-events: none; bottom: 0px; right: 0px;"><div style="border: 0px none; margin: 0px; padding: 0px; pointer-events: none; float: right; height: 20px;"><div style="position: relative; width: 53px; height: 14px; margin: 0px 12px 6px 2px; overflow: hidden; pointer-events: auto;"><span style="display: block; margin: 0px; padding: 0px 4px; text-align: center; font-size: 10px; line-height: 11px; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; font-weight: 700; color: rgb(34, 34, 37); text-shadow: rgba(255, 255, 255, 0.8) -1px 0px, rgba(255, 255, 255, 0.8) 0px 1px, rgba(255, 255, 255, 0.8) 1px 0px, rgba(255, 255, 255, 0.8) 0px -1px;">50m</span><img src="https://ssl.pstatic.net/static/maps/mantle/2x/new-scale-normal-b.png" width="47" height="3" alt="" style="position: absolute; left: 3px; bottom: 0px; z-index: 2; display: block; width: 47px; height: 3px; overflow: hidden; margin: 0px; padding: 0px; border: 0px none; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/new-scale-normal-l.png" width="3" height="8" alt="" style="position:absolute;left:0;bottom:0;z-index:2;display:block;width:3px;height:8px;overflow:hidden;margin:0;padding:0;border:0 none;max-width:none !important;max-height:none !important;min-width:0 !important;min-height:0 !important;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/new-scale-normal-r.png" width="3" height="8" alt="" style="position:absolute;right:0;bottom:0;z-index:2;display:block;width:3px;height:8px;overflow:hidden;margin:0;padding:0;border:0 none;max-width:none !important;max-height:none !important;min-width:0 !important;min-height:0 !important;"></div></div></div><div style="position: absolute; z-index: 100; margin: 0px; padding: 0px; pointer-events: none; bottom: 0px; left: 0px;"><div style="border: 0px none; margin: 0px; padding: 0px; pointer-events: none; float: left; height: 21px;"><div class="map_copyright" style="margin: 0px; padding: 0px 0px 2px 10px; height: 19px; line-height: 19px; color: rgb(68, 68, 68); font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; font-size: 11px; clear: both; white-space: nowrap; pointer-events: none;"><div style="float: left;"><span style="white-space: pre; color: rgb(68, 68, 68);">© NAVER Corp.</span></div><a href="#" style="font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; font-size: 11px; line-height: 19px; margin: 0px 0px 0px 5px; padding: 0px; color: rgb(68, 68, 68); float: left; pointer-events: auto; text-decoration: underline; display: none;">더보기</a><div style="float: left;"><a target="_blank" href="http://www.openstreetmap.org/copyright" style="pointer-events: auto; white-space: pre; display: none; color: rgb(68, 68, 68);"> /OpenStreetMap</a></div></div></div></div><div style="border: 1px solid rgb(41, 41, 48); background: rgb(255, 255, 255); padding: 15px; color: rgb(51, 51, 51); position: absolute; font-size: 11px; line-height: 1.5; clear: both; display: none; max-width: 350px !important; max-height: 300px !important;"><h5 style="font-size: 12px; margin-top: 0px; margin-bottom: 10px;">지도 데이터</h5><a href="#" style="position: absolute; top: 8px; right: 8px; width: 14px; height: 14px; font-size: 14px; line-height: 14px; display: block; overflow: hidden; color: rgb(68, 68, 68); text-decoration: none; font-weight: bold; text-align: center;">x</a><div><span style="white-space: pre; color: rgb(68, 68, 68); float: left;">© NAVER Corp.</span><a target="_blank" href="http://www.openstreetmap.org/copyright" style="pointer-events: auto; white-space: pre; color: rgb(68, 68, 68); float: left; display: none;"> /OpenStreetMap</a></div></div><div style="position: absolute; z-index: 100; margin: 0px; padding: 0px; pointer-events: none; top: 0px; right: 0px;"><div style="border: 0px none; margin: 0px; padding: 0px; pointer-events: none; float: right;"><div style="position: relative; z-index: 3; pointer-events: auto;"><div style="position: relative; z-index: 0; width: 28px; margin: 10px; border: 1px solid rgb(68, 68, 68); box-sizing: content-box !important; user-select: none;"><a href="#" style="position: relative; z-index: 2; width: 28px; height: 28px; cursor: pointer; display: block; overflow: hidden; border-bottom: 0px none; box-sizing: content-box !important;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-in-small-normal.png" width="28" height="28" alt="지도 확대" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 28px; height: 28px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"></a><div style="position: relative; width: 28px; height: 216px; overflow: hidden; margin: 0px; padding: 7px 0px; background-color: rgb(255, 255, 255); cursor: pointer; box-sizing: content-box !important; display: none;"><div style="position: absolute; top: 7px; bottom: 7px; left: 12px; width: 4px; height: 216px; display: block; background-color: rgb(47, 135, 236);"></div><div style="position: absolute; top: 7px; bottom: 7px; left: 12px; width: 4px; height: 44px; display: block; background-color: rgb(202, 205, 209);"></div><a href="#" style="position: absolute; left: 4px; width: 18px; height: 10px; top: 44px; border: 1px solid rgb(68, 68, 68); cursor: move; display: block; overflow: hidden; box-sizing: content-box !important;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-handle.png" width="18" height="10" alt="지도 확대/축소 슬라이더" style="margin:0;padding:0;border:solid 0 transparent;display:block;box-sizing:content-box !important;max-width:none !important;max-height:none !important;min-width:0 !important;min-height:0 !important;width:18px;height:10px;"></a></div><a href="#" style="position: relative; z-index: 2; width: 28px; height: 28px; cursor: pointer; display: block; overflow: hidden; border-top: 1px solid rgb(202, 205, 209); box-sizing: content-box !important;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-out-small-normal.png" width="28" height="28" alt="지도 축소" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 28px; height: 28px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"></a><div style="position: absolute; top: 22px; width: 44px; height: 0px; overflow: visible; display: none; left: -51px;"><div style="display: block; margin: 0px; padding: 0px;"><h4 style="visibility:hidden;width:0;height:0;overflow:hidden;margin:0;padding:0;">지도 컨트롤러 범례</h4><div style="position: absolute; top: 43px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-on.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">부동산</span></div><div style="position: absolute; top: 63px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-normal.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">거리</span></div><div style="position: absolute; top: 83px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-normal.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">읍,면,동</span></div><div style="position: absolute; top: 113px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-normal.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">시,군,구</span></div><div style="position: absolute; top: 143px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-normal.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">시,도</span></div><div style="position: absolute; top: 163px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-normal.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">국가</span></div></div></div></div></div></div></div></div>
                                    <img src="https://simg.pstatic.net/static.map/v2/map/staticmap.bin?caller=smarteditor&amp;markers=pos%3A126.9371352%2037.4841255%7CviewSizeRatio%3A0.7%7Ctype%3Ad%7Ccolor%3A0x11cc73%7Csize%3Amid&amp;w=700&amp;h=315&amp;scale=2&amp;dataversion=174.37" alt="" class="se-map-image egjs-visible" style="display: none;">
                                </div>
                                    <div class="se-module se-module-map-text ">
                                            <a href="#" target="_blank" class="se-map-info __se_link" onclick="return false;" data-linktype="map" data-linkdata="{&quot;eventTarget&quot; : &quot;placeDesc&quot;, &quot;placeId&quot; : &quot;1775787333&quot;, &quot;searchEngine&quot; : &quot;naver&quot;, &quot;searchType&quot; : &quot;s&quot;, &quot;name&quot; : &quot;중화요리 팔공&quot;, &quot;address&quot; : &quot;서울특별시 관악구 남부순환로 1680&quot;, &quot;latitude&quot; : &quot;37.4841255&quot;, &quot;longitude&quot; : &quot;126.9371352&quot;, &quot;tel&quot; : &quot;0507-1307-9815&quot;, &quot;bookingUrl&quot; : null }">
                                            <strong class="se-map-title">중화요리 팔공</strong>
                                            <p class="se-map-address">서울특별시 관악구 남부순환로 1680</p>
                                        </a>
                                    </div>
                            
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module="{&quot;type&quot;:&quot;v2_map&quot;, &quot;id&quot; :&quot;SE-c2000acc-2f91-4e07-8259-9963e40aae73&quot;, &quot;data&quot; : { &quot;layout&quot;: &quot;default&quot;, &quot;searchEngine&quot; : &quot;naver&quot;, &quot;places&quot; : [{&quot;placeId&quot;:&quot;1775787333&quot;,&quot;name&quot;:&quot;중화요리 팔공&quot;,&quot;address&quot;:&quot;서울특별시 관악구 남부순환로 1680&quot;,&quot;latlng&quot;:{&quot;@ctype&quot;:&quot;position&quot;,&quot;latitude&quot;:37.4841255,&quot;longitude&quot;:126.9371352},&quot;searchType&quot;:&quot;s&quot;,&quot;tel&quot;:&quot;0507-1307-9815&quot;,&quot;bookingUrl&quot;:null}] }}" data-module-v2="{&quot;type&quot;:&quot;v2_map&quot;, &quot;id&quot; :&quot;SE-c2000acc-2f91-4e07-8259-9963e40aae73&quot;, &quot;data&quot; : { &quot;layout&quot;: &quot;default&quot;, &quot;searchEngine&quot; : &quot;naver&quot;, &quot;places&quot; : [{&quot;placeId&quot;:&quot;1775787333&quot;,&quot;name&quot;:&quot;중화요리 팔공&quot;,&quot;address&quot;:&quot;서울특별시 관악구 남부순환로 1680&quot;,&quot;latlng&quot;:{&quot;@ctype&quot;:&quot;position&quot;,&quot;latitude&quot;:37.4841255,&quot;longitude&quot;:126.9371352},&quot;searchType&quot;:&quot;s&quot;,&quot;tel&quot;:&quot;0507-1307-9815&quot;,&quot;bookingUrl&quot;:null}] }}"></script>
                    </div>                <div class="se-component se-text se-l-default" id="SE-80d4c6a5-4a37-11f0-b773-1125b60cd3a9">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-7ad1ec8c-4e0a-44b1-a4f0-5f61b050295d"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d639085-4a37-11f0-b773-e547e4a13bfd"> </span><span style="color:#1808f9;" class="se-fs-fs19 se-ff-nanummaruburi   " id="SE-9d639086-4a37-11f0-b773-1d5fb729cdb2"><b>오랜만에 오셨네요 하셔서  " 이젠 와인 못 마시겠네요 "했더니 웃으시더군요 ㅎ </b></span><span style="color:#1808f9;" class="se-fs-fs19 se-ff-nanumbarungothic   " id="SE-9d639087-4a37-11f0-b773-c92a23f62784"><b>&ZeroWidthSpace;</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-6f0f49d3-b15a-48b0-a21f-95426aace724"><span style="color:#1808f9;" class="se-fs-fs19 se-ff-nanumbarungothic   " id="SE-9d639088-4a37-11f0-b773-2118b7f412ff"><b>&ZeroWidthSpace;</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-8090c1d7-16ca-4871-9af8-7b77ae3298d0"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d639089-4a37-11f0-b773-edc218a82c24"><a href="https://blog.naver.com/melburne/222278591313" class="se-link __se_link" data-linktype="text" data-linkdata="{&quot;id&quot;: &quot;SE-9d639089-4a37-11f0-b773-edc218a82c24&quot;, &quot;link&quot;: &quot;https://blog.naver.com/melburne/222278591313&quot;}" target="_blank">https://blog.naver.com/melburne/222278591313</a></span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-80d4c6a5-4a37-11f0-b773-1125b60cd3a9&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-oglink se-l-large_image __se-component" id="SE-030a38b7-bfeb-4c2e-be8f-e4bfabe37875">
                        <div class="se-component-content">
                            <div class="se-section se-section-oglink se-l-large_image se-section-align-center">
                                <div class="se-module se-module-oglink">
                                    <a href="https://blog.naver.com/melburne/222278591313" class="se-oglink-thumbnail __se_link" target="_blank" data-linktype="oglink" data-linkdata="{&quot;id&quot;: &quot;SE-030a38b7-bfeb-4c2e-be8f-e4bfabe37875&quot;, &quot;link&quot;: &quot;https://blog.naver.com/melburne/222278591313&quot;}">
                                        <img src="https://dthumb-phinf.pstatic.net/?src=%22https%3A%2F%2Fblogthumb.pstatic.net%2FMjAyMTAzMTdfMTc5%2FMDAxNjE1OTU0MzExNjk0.cMTgZYYDLJQ_Goj_jaZIbc_AOL3CSCLA7cNMIn0OfeMg.VA9uLe9Ec9V7JW1Y-D5civB_64di8BcbhedM-p4AEngg.JPEG.melburne%2F20210109_172323.jpg%3Ftype%3Dw2%22&amp;type=ff500_300" class="se-oglink-thumbnail-resource egjs-visible" alt="">
                                    </a>
                                    <a href="https://blog.naver.com/melburne/222278591313" class="se-oglink-info __se_link" target="_blank" data-linktype="oglink" data-linkdata="{&quot;id&quot;: &quot;SE-030a38b7-bfeb-4c2e-be8f-e4bfabe37875&quot;, &quot;link&quot;: &quot;https://blog.naver.com/melburne/222278591313&quot;}">
                                        <div class="se-oglink-info-container">
                                            <strong class="se-oglink-title">[팔공/봉천] - 이 동네에서 꽤 잘하는 중국집</strong>
                                            <p class="se-oglink-summary">팔공 형님들과 와인한잔을 하기로 하고 장소를 물색합니다. 에전부터 가봐야지 했던 곳인데 이날 인연이 되...</p>
                                            <p class="se-oglink-url">blog.naver.com</p>
                                        </div>
                                    </a>
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module="{&quot;type&quot;:&quot;v2_oglink&quot;, &quot;id&quot; :&quot;SE-030a38b7-bfeb-4c2e-be8f-e4bfabe37875&quot;, &quot;data&quot; : {&quot;link&quot; : &quot;https://blog.naver.com/melburne/222278591313&quot;, &quot;isVideo&quot; : &quot;false&quot;, &quot;thumbnail&quot; : &quot;https://dthumb-phinf.pstatic.net/?src=%22https%3A%2F%2Fblogthumb.pstatic.net%2FMjAyMTAzMTdfMTc5%2FMDAxNjE1OTU0MzExNjk0.cMTgZYYDLJQ_Goj_jaZIbc_AOL3CSCLA7cNMIn0OfeMg.VA9uLe9Ec9V7JW1Y-D5civB_64di8BcbhedM-p4AEngg.JPEG.melburne%2F20210109_172323.jpg%3Ftype%3Dw2%22&amp;type=ff500_300&quot;}}" data-module-v2="{&quot;type&quot;:&quot;v2_oglink&quot;, &quot;id&quot; :&quot;SE-030a38b7-bfeb-4c2e-be8f-e4bfabe37875&quot;, &quot;data&quot; : {&quot;link&quot; : &quot;https://blog.naver.com/melburne/222278591313&quot;, &quot;isVideo&quot; : &quot;false&quot;, &quot;thumbnail&quot; : &quot;https://dthumb-phinf.pstatic.net/?src=%22https%3A%2F%2Fblogthumb.pstatic.net%2FMjAyMTAzMTdfMTc5%2FMDAxNjE1OTU0MzExNjk0.cMTgZYYDLJQ_Goj_jaZIbc_AOL3CSCLA7cNMIn0OfeMg.VA9uLe9Ec9V7JW1Y-D5civB_64di8BcbhedM-p4AEngg.JPEG.melburne%2F20210109_172323.jpg%3Ftype%3Dw2%22&amp;type=ff500_300&quot;}}"></script>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-0084d209-4143-458d-bd0d-d67a4882827c">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-519237b2-9d0c-4c73-bb54-a707355ceb69"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63b79a-4a37-11f0-b773-83190eabe637">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-6b50d816-1d0a-46c2-bcf6-5d2408554c0f"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63b79b-4a37-11f0-b773-01c9a2143d0b">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-1fd7b1e7-d93c-448a-9f69-db1fa59cc248"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63b79c-4a37-11f0-b773-f5b7cef774b2"><a href="https://blog.naver.com/melburne/222860854461" class="se-link __se_link" data-linktype="text" data-linkdata="{&quot;id&quot;: &quot;SE-9d63b79c-4a37-11f0-b773-f5b7cef774b2&quot;, &quot;link&quot;: &quot;https://blog.naver.com/melburne/222860854461&quot;}" target="_blank">https://blog.naver.com/melburne/222860854461</a></span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-0084d209-4143-458d-bd0d-d67a4882827c&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-oglink se-l-large_image __se-component" id="SE-aeeb33fe-8f08-4d5f-bb8c-4e9df696536b">
                        <div class="se-component-content">
                            <div class="se-section se-section-oglink se-l-large_image se-section-align-center">
                                <div class="se-module se-module-oglink">
                                    <a href="https://blog.naver.com/melburne/222860854461" class="se-oglink-thumbnail __se_link" target="_blank" data-linktype="oglink" data-linkdata="{&quot;id&quot;: &quot;SE-aeeb33fe-8f08-4d5f-bb8c-4e9df696536b&quot;, &quot;link&quot;: &quot;https://blog.naver.com/melburne/222860854461&quot;}">
                                        <img src="https://dthumb-phinf.pstatic.net/?src=%22https%3A%2F%2Fblogthumb.pstatic.net%2FMjAyMjA4MjNfMjMg%2FMDAxNjYxMjUxNTAwNTM5.HxDHbBhPrLxrCAq5ATV6pFlTBGNJHQ4AMFF-fnewMLcg.VNbnf_EfeTdMCbXYk86sQKQTRyN-53myGuQabv8dC4Ig.JPEG.melburne%2F20220601_170559.jpg%3Ftype%3Dw2%22&amp;type=ff500_300" class="se-oglink-thumbnail-resource egjs-visible" alt="">
                                    </a>
                                    <a href="https://blog.naver.com/melburne/222860854461" class="se-oglink-info __se_link" target="_blank" data-linktype="oglink" data-linkdata="{&quot;id&quot;: &quot;SE-aeeb33fe-8f08-4d5f-bb8c-4e9df696536b&quot;, &quot;link&quot;: &quot;https://blog.naver.com/melburne/222860854461&quot;}">
                                        <div class="se-oglink-info-container">
                                            <strong class="se-oglink-title">[팔공/봉천동] - 줄을 서는 건 이유가 있어서야~</strong>
                                            <p class="se-oglink-summary">팔공 TV에 나온 집이나 요즘은 유투브가 대세라고 하던데 암튼 그런 집들은 잠시 대기가 생기고 했다가 ...</p>
                                            <p class="se-oglink-url">blog.naver.com</p>
                                        </div>
                                    </a>
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module="{&quot;type&quot;:&quot;v2_oglink&quot;, &quot;id&quot; :&quot;SE-aeeb33fe-8f08-4d5f-bb8c-4e9df696536b&quot;, &quot;data&quot; : {&quot;link&quot; : &quot;https://blog.naver.com/melburne/222860854461&quot;, &quot;isVideo&quot; : &quot;false&quot;, &quot;thumbnail&quot; : &quot;https://dthumb-phinf.pstatic.net/?src=%22https%3A%2F%2Fblogthumb.pstatic.net%2FMjAyMjA4MjNfMjMg%2FMDAxNjYxMjUxNTAwNTM5.HxDHbBhPrLxrCAq5ATV6pFlTBGNJHQ4AMFF-fnewMLcg.VNbnf_EfeTdMCbXYk86sQKQTRyN-53myGuQabv8dC4Ig.JPEG.melburne%2F20220601_170559.jpg%3Ftype%3Dw2%22&amp;type=ff500_300&quot;}}" data-module-v2="{&quot;type&quot;:&quot;v2_oglink&quot;, &quot;id&quot; :&quot;SE-aeeb33fe-8f08-4d5f-bb8c-4e9df696536b&quot;, &quot;data&quot; : {&quot;link&quot; : &quot;https://blog.naver.com/melburne/222860854461&quot;, &quot;isVideo&quot; : &quot;false&quot;, &quot;thumbnail&quot; : &quot;https://dthumb-phinf.pstatic.net/?src=%22https%3A%2F%2Fblogthumb.pstatic.net%2FMjAyMjA4MjNfMjMg%2FMDAxNjYxMjUxNTAwNTM5.HxDHbBhPrLxrCAq5ATV6pFlTBGNJHQ4AMFF-fnewMLcg.VNbnf_EfeTdMCbXYk86sQKQTRyN-53myGuQabv8dC4Ig.JPEG.melburne%2F20220601_170559.jpg%3Ftype%3Dw2%22&amp;type=ff500_300&quot;}}"></script>
                    </div>
                    <div class="se-component se-image se-l-default __se-component" id="SE-622effbd-9887-4772-9916-edd8c1146e35">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-center">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-622effbd-9887-4772-9916-edd8c1146e35&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfMjUw/MDAxNzQ5OTQ0MjI4NzU3.e7ZLwfi-oY8vE-oBkKkfSFcIVlDQRL7d_v_Qip70cgMg.slTFy9KkAfP3rzzgjrRSspOEnsH7UN-xm2_DvikHoPUg.JPEG/SE-622effbd-9887-4772-9916-edd8c1146e35.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfMjUw/MDAxNzQ5OTQ0MjI4NzU3.e7ZLwfi-oY8vE-oBkKkfSFcIVlDQRL7d_v_Qip70cgMg.slTFy9KkAfP3rzzgjrRSspOEnsH7UN-xm2_DvikHoPUg.JPEG/SE-622effbd-9887-4772-9916-edd8c1146e35.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-622effbd-9887-4772-9916-edd8c1146e35_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-622effbd-9887-4772-9916-edd8c1146e35&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-80d4c6a2-4a37-11f0-b773-3db526716dc8">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-4b52692c-c259-4d00-b3b5-c1eb37fefb84"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63b79d-4a37-11f0-b773-d768c9c3c1ed">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-47963997-50e0-48dc-8cea-c0bf92652d41"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63b79e-4a37-11f0-b773-61950a4aefa0">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-cba66fbb-279d-40f9-b9e5-fee0b8c08be4"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63b79f-4a37-11f0-b773-db16f8e9036f">차림료</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-462e66a7-39ad-4886-a1eb-6b281aae1c86"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63b7a0-4a37-11f0-b773-d9460fd46024">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-53670df1-08e0-4357-8793-a030c9003b0e"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63b7a1-4a37-11f0-b773-3bcab71ad974">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-80d4c6a2-4a37-11f0-b773-3db526716dc8&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-image se-l-default __se-component" id="SE-49e6d64e-9916-463d-926a-bc6b765b5e49">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-49e6d64e-9916-463d-926a-bc6b765b5e49&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTFfMjU3/MDAxNzQ5NjM3NDAzMjU0.WXr5WtS0RT8w0YsMZqu0ZBP_JcbctBuZWRojh4KMDewg.p-QonglWnp9M06VVOu5FGuVcBs_ph4G5P8D2nxn-CAcg.JPEG/20250611_142216.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTFfMjU3/MDAxNzQ5NjM3NDAzMjU0.WXr5WtS0RT8w0YsMZqu0ZBP_JcbctBuZWRojh4KMDewg.p-QonglWnp9M06VVOu5FGuVcBs_ph4G5P8D2nxn-CAcg.JPEG/20250611_142216.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-49e6d64e-9916-463d-926a-bc6b765b5e49_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-49e6d64e-9916-463d-926a-bc6b765b5e49&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-80d4c69f-4a37-11f0-b773-0d06796a5e13">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-4030e791-85fd-4308-91d5-e12dff814bca"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63b7a2-4a37-11f0-b773-975c7578f7c7">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-cc6e77ad-b565-46ba-b37f-0eb66bdf74cc"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63b7a3-4a37-11f0-b773-734ff0452b36">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-e6c59bc4-4d92-4834-bbe1-841d55ea7b1e"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63deb4-4a37-11f0-b773-71487b73fbcc"><b>밑반찬들 ㅎ</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-eaf86d5e-9bc8-4c64-8a59-b8736a2c43ee"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63deb5-4a37-11f0-b773-7135000ea387">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-3de5440b-6393-4580-937b-142a749a50d9"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63deb6-4a37-11f0-b773-73d0207caa4f">요즘 짜사이 주는 곳 참 좋아합니다. 어디였더라? 짜사이가 엄청 맛있었던 곳이 얼마 전 있었는데 음.</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-80d4c69f-4a37-11f0-b773-0d06796a5e13&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="ssp-adcontent align_center"><div id="ssp-adcontent-1" class="ssp_adcontent_inner"><div style="width: 100%; height: auto; margin: 0px auto; line-height: 0;"><iframe id="ssp-adcontent-1_tgtLREC" frameborder="no" scrolling="no" tabindex="0" name="" title="AD" style="width: 100%; height: 170px; visibility: inherit; border: 0px; vertical-align: bottom;"></iframe></div></div></div><div class="se-component se-image se-l-default __se-component" id="SE-714fc968-2004-405f-8115-7b9be46a5d77">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-714fc968-2004-405f-8115-7b9be46a5d77&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTFfMjQy/MDAxNzQ5NjM3MzcyNjIz.DfGOlrfIkkvYoI_AyLuBc_k2OYnlKOcYjTdUoDkQAZog.uS15QQ8iXFzjlXerILzN85HsVtfnz9TGbxfPb7SXQgsg.JPEG/20250611_142539.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTFfMjQy/MDAxNzQ5NjM3MzcyNjIz.DfGOlrfIkkvYoI_AyLuBc_k2OYnlKOcYjTdUoDkQAZog.uS15QQ8iXFzjlXerILzN85HsVtfnz9TGbxfPb7SXQgsg.JPEG/20250611_142539.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-714fc968-2004-405f-8115-7b9be46a5d77_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-714fc968-2004-405f-8115-7b9be46a5d77&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-80d4c69c-4a37-11f0-b773-a12b240f6674">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-d675b5dc-d606-4b0f-9ce3-419409f6815d"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63deb7-4a37-11f0-b773-c7f6f04c743b">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-6810db23-c81e-4b1f-a1ca-02104812af16"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63deb8-4a37-11f0-b773-c9f927267c4f">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-d83b9223-103f-4538-b001-99649ed56407"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63deb9-4a37-11f0-b773-4d917c573a7f"><b>옛날볶음밥(12,000원)</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-9ddd101c-e97b-4bfa-ab7a-7ae2a4c292f6"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63deba-4a37-11f0-b773-d7fd0e6e7ab2">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-e4276bc0-235f-4af1-864f-4f78ee8fb985"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63debb-4a37-11f0-b773-459895da3bb4">불맛나고 고슬고슬 잘 볶아낸 볶음밥에 바로 볶아서 내어주는 짜장까지 정말이지 훌륭한 볶음밥입니다. 오랜만에 만나다보니 흥문을 ㅎ</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-3406259b-e740-43ed-9227-ffa4aa498a0b"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63debc-4a37-11f0-b773-e5bca6ceaf12">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-80d4c69c-4a37-11f0-b773-a12b240f6674&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-image se-l-default __se-component" id="SE-b88eecfd-410e-4f3a-923f-cdb8bb344c5b">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-b88eecfd-410e-4f3a-923f-cdb8bb344c5b&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTFfODkg/MDAxNzQ5NjM3MzcyMzcz.iRvFVcUMUSYF-9ZsM97etnI1yfZK-z4rmoHvoTUDBkcg.J7BEQc3IUNLmK24l7gnlGnqvOHlP1eibjjIt2h-eTC0g.JPEG/20250611_142533.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTFfODkg/MDAxNzQ5NjM3MzcyMzcz.iRvFVcUMUSYF-9ZsM97etnI1yfZK-z4rmoHvoTUDBkcg.J7BEQc3IUNLmK24l7gnlGnqvOHlP1eibjjIt2h-eTC0g.JPEG/20250611_142533.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-b88eecfd-410e-4f3a-923f-cdb8bb344c5b_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-b88eecfd-410e-4f3a-923f-cdb8bb344c5b&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-13f58325-f0d3-4394-aedf-d60956de3e88">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-e2d25c3d-0979-4b48-adbf-ad930956dafb"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63debd-4a37-11f0-b773-7d2d69094f99">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-c4a04474-8251-4de5-b721-392138a5e832"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63debe-4a37-11f0-b773-6ff083c7326b">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-ca06a9ff-2054-4e5f-b6ee-714fed928dde"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63debf-4a37-11f0-b773-354571c883f0">고슬고슬 기름기 없이 볶아내서 내어주십니다. 3명이서 총 4개의 메뉴를 주문했습니다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-1812cb88-36df-46c0-beea-cc1d658ddba0"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63dec0-4a37-11f0-b773-c19f8ec1b7d3">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-647143bd-b226-4f29-9ff4-ab1046f4f2e8"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63dec1-4a37-11f0-b773-ed1de1088612">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-13f58325-f0d3-4394-aedf-d60956de3e88&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-image se-l-default __se-component" id="SE-59b69531-a44a-4e62-afaa-c60933d91c64">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-59b69531-a44a-4e62-afaa-c60933d91c64&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTFfMjAx/MDAxNzQ5NjM3MzcxMTI4.u7SvJL3B_lpCMpy6nDUFxceu-pL5TZMYhHEX-xIXLCAg.DCac9ZE8VKol3Ke3xfOrkSlQqsDaMplXwaRkDtcTX4Yg.JPEG/20250611_142535.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTFfMjAx/MDAxNzQ5NjM3MzcxMTI4.u7SvJL3B_lpCMpy6nDUFxceu-pL5TZMYhHEX-xIXLCAg.DCac9ZE8VKol3Ke3xfOrkSlQqsDaMplXwaRkDtcTX4Yg.JPEG/20250611_142535.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-59b69531-a44a-4e62-afaa-c60933d91c64_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-59b69531-a44a-4e62-afaa-c60933d91c64&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-1ea92654-4dd3-4a5a-b300-b82ba300ac23">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-b87f9c02-b31d-466d-8550-26363cbdd740"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d63dec2-4a37-11f0-b773-177f3b9cfe65">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-4add28eb-e558-4206-8b45-b6b7d7cbcfee"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d6405d3-4a37-11f0-b773-074abdb6b7c9">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-7aa3844d-e2a3-4443-a6f4-711797273397"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d6405d4-4a37-11f0-b773-13407b9c65f9">후라이가 아쉽네요. 튀긴 옛날 후라이가 좋은데 아습입니다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-a6c97280-c3fb-4bfc-99be-61d39f63c01c"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d6405d5-4a37-11f0-b773-f54bd5a66c2c">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-1ea92654-4dd3-4a5a-b300-b82ba300ac23&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-image se-l-default __se-component" id="SE-1d9baf83-40f9-4b4f-bfa3-14a732bf78a3">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-1d9baf83-40f9-4b4f-bfa3-14a732bf78a3&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfMjE5/MDAxNzQ5OTQ0MTY1NzU3.b2Gi97-3Y7X12-n8jYcI7SGDIhTsh8E05sfa4MmS0Wcg.0_bv2Sze0k3yLe0FNt2qEFBSNjN5BbuKMB4Yj6lg_Ssg.JPEG/20250611_142223.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfMjE5/MDAxNzQ5OTQ0MTY1NzU3.b2Gi97-3Y7X12-n8jYcI7SGDIhTsh8E05sfa4MmS0Wcg.0_bv2Sze0k3yLe0FNt2qEFBSNjN5BbuKMB4Yj6lg_Ssg.JPEG/20250611_142223.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-1d9baf83-40f9-4b4f-bfa3-14a732bf78a3_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-1d9baf83-40f9-4b4f-bfa3-14a732bf78a3&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-63af0e0b-30c4-4c14-b825-550ab8ab8b97">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-d722ae38-0028-4a41-b5f3-69ff6ef212ab"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d6405d6-4a37-11f0-b773-19db90c31bea">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-b8ae620d-aeaa-4fd1-9455-d03c5f39fcf0"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d6405d7-4a37-11f0-b773-8f07056e927d">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-565f9e52-11a6-4d48-835a-c701d79c4dcd"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d6405d8-4a37-11f0-b773-07ee03cec94f">이집 계란국도 헛투루 내어주지 않으십니다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-0fb2ae1a-fce8-4954-8014-49f5ee804b24"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d6405d9-4a37-11f0-b773-5dfb82ce6350">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-4c943c7a-c492-4535-828b-b9fa883fbc1d"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d6405da-4a37-11f0-b773-79e96068be32">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-63af0e0b-30c4-4c14-b825-550ab8ab8b97&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-image se-l-default __se-component" id="SE-0fc504de-7e04-468c-8409-4f060939d675">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-0fc504de-7e04-468c-8409-4f060939d675&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTFfMjk0/MDAxNzQ5NjM3MzczNDMw.4xYjr9uqmpSSC0QnRoK4qs3uJrgl4YIcIpW-nfOdplQg.fLEp8CkVwOjTt9kJ-tH7ipUEzNJ-40aQNiWX9aYADWwg.JPEG/20250611_142709.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTFfMjk0/MDAxNzQ5NjM3MzczNDMw.4xYjr9uqmpSSC0QnRoK4qs3uJrgl4YIcIpW-nfOdplQg.fLEp8CkVwOjTt9kJ-tH7ipUEzNJ-40aQNiWX9aYADWwg.JPEG/20250611_142709.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-0fc504de-7e04-468c-8409-4f060939d675_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-0fc504de-7e04-468c-8409-4f060939d675&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-4f14a5f9-801a-4cd0-8cf2-860e5331b44d">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-f17bd91b-9c7f-4e4c-89c9-53ef92c37ce6"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d6405db-4a37-11f0-b773-852b0caae34e">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-724f8469-d844-43d6-94fe-bc0684e07d97"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d6405dc-4a37-11f0-b773-9577f2198e54">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-2a65f3fe-0fed-4b14-97ff-f68b611894f4"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d6405dd-4a37-11f0-b773-6f76ff344cfe">짜장과 함께 먹는 볶음밥은 역시 굿입니다. 맛나네요.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-0056f25e-6add-441a-aef0-aa095c8d38b2"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d6405de-4a37-11f0-b773-879f73433c97">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-5c52b798-36f3-4d42-9dfa-3dbdb07b1272"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d6405df-4a37-11f0-b773-37f6aa421d55">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-4f14a5f9-801a-4cd0-8cf2-860e5331b44d&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-image se-l-default __se-component" id="SE-9aba2384-e4ff-47cd-b6a6-28a5a4a09fe7">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-9aba2384-e4ff-47cd-b6a6-28a5a4a09fe7&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTFfMTEy/MDAxNzQ5NjM3MzgxMjk5.lHDMT9EZCXqYslqS7RuFh8RhhTQ8vVrIgjZudDGOTHIg.LSnXJJjCzWMZxp9qesrjWX-3wVMv5YIlsMu_nibboawg.JPEG/20250611_142853.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTFfMTEy/MDAxNzQ5NjM3MzgxMjk5.lHDMT9EZCXqYslqS7RuFh8RhhTQ8vVrIgjZudDGOTHIg.LSnXJJjCzWMZxp9qesrjWX-3wVMv5YIlsMu_nibboawg.JPEG/20250611_142853.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-9aba2384-e4ff-47cd-b6a6-28a5a4a09fe7_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-9aba2384-e4ff-47cd-b6a6-28a5a4a09fe7&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-80d4c699-4a37-11f0-b773-1d76ce662946">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-40b8bfe8-d5e7-4b9e-8d04-5c655a45a580"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d642cf0-4a37-11f0-b773-d33e150b63e3">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-1ac91deb-0706-4163-8379-0fa6050dfbcc"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d642cf1-4a37-11f0-b773-031ebe7462df">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-557d5b5c-ce3a-446f-a4cc-e8c31bfa5533"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d642cf2-4a37-11f0-b773-cb011a51cb34"><b>짜장면(10.000원)</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-1d51a297-475d-421e-8e2b-af6025c06480"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d642cf3-4a37-11f0-b773-c7dffe109e78">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-22f72e87-4820-4ab9-bf13-18ba65501de7"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d642cf4-4a37-11f0-b773-fd77197b320c">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-80d4c699-4a37-11f0-b773-1d76ce662946&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-image se-l-default __se-component" id="SE-a54d73d7-b18b-4f45-a7dd-da5e5c68063d">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-a54d73d7-b18b-4f45-a7dd-da5e5c68063d&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTFfMjU2/MDAxNzQ5NjM3MzgzNjQ5.7CG6L-lTbCzjTxzBeqZFkOy9lqATSiPW-vqdOchGrRgg.OdiN1rcXB_g_VC2Ul6armYQC558F_tJYrjJUNc2hufgg.JPEG/20250611_142855.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTFfMjU2/MDAxNzQ5NjM3MzgzNjQ5.7CG6L-lTbCzjTxzBeqZFkOy9lqATSiPW-vqdOchGrRgg.OdiN1rcXB_g_VC2Ul6armYQC558F_tJYrjJUNc2hufgg.JPEG/20250611_142855.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-a54d73d7-b18b-4f45-a7dd-da5e5c68063d_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-a54d73d7-b18b-4f45-a7dd-da5e5c68063d&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="ssp-adcontent align_center"><div id="ssp-adcontent-2" class="ssp_adcontent_inner"><div style="width: 100%; height: auto; margin: 0px auto; line-height: 0;"><iframe id="ssp-adcontent-2_tgtLREC" frameborder="no" scrolling="no" tabindex="0" name="" title="AD" style="width: 100%; height: 170px; visibility: inherit; border: 0px; vertical-align: bottom;"></iframe></div></div></div><div class="se-component se-text se-l-default" id="SE-a5f3f035-90dc-4dc6-bcfb-e304e50a5b34">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-73038ca3-e29c-4a23-b56f-2e981789926c"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d642cf5-4a37-11f0-b773-11ec8e7241ec">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-ade407e1-d313-4944-8664-d39d6c71d9ae"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d642cf6-4a37-11f0-b773-294d93f90a36">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-8b37954d-2f4c-4717-ac65-2564867106a5"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d642cf7-4a37-11f0-b773-0b9d1ae24688">일반짜장면이라고 하기보다는 채소도 큼직한 간짜장이라고 보시는 게 맞을 거 같습니다,.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-8256d2af-16b5-48e9-9023-9a49f0bc67c1"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d642cf8-4a37-11f0-b773-638f128e5128">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-dca078b6-ada0-484c-9feb-f7d4fb17a27a"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d642cf9-4a37-11f0-b773-49dfc4bfbc5b">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-a5f3f035-90dc-4dc6-bcfb-e304e50a5b34&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-image se-l-default __se-component" id="SE-13176ffa-0494-4108-981b-4e357a9b9a3b">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-13176ffa-0494-4108-981b-4e357a9b9a3b&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTFfMjA2/MDAxNzQ5NjM3Mzc5ODky.QyLgN5K2Lr9zf7pyWu_r8mSHjb-fpKmOE0Y3eymlEOIg.qEiC86GoxIlhj2J0VMKLC4vgKh-ai2NIn6GVj3XpyDUg.JPEG/20250611_142935.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTFfMjA2/MDAxNzQ5NjM3Mzc5ODky.QyLgN5K2Lr9zf7pyWu_r8mSHjb-fpKmOE0Y3eymlEOIg.qEiC86GoxIlhj2J0VMKLC4vgKh-ai2NIn6GVj3XpyDUg.JPEG/20250611_142935.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-13176ffa-0494-4108-981b-4e357a9b9a3b_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-13176ffa-0494-4108-981b-4e357a9b9a3b&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-56f429b9-5077-4161-b94b-dc5cd68b537f">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-ade99485-f74a-4cd5-a9fd-c73a6119ec70"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d642cfa-4a37-11f0-b773-abd9a7881257">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-0576a36a-bd5e-4b67-9d73-3ac9e1e4f8bd"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d642cfb-4a37-11f0-b773-6f9498ea745b">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-201430c4-021c-45ee-b0c1-4ece6d02645d"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d642cfc-4a37-11f0-b773-15ba837990cf">면에 짜장이 잘 베이면서 진득한게 끝내주죠. 저는 한 젓가락 조금 얻어서 맛을 봤는데 역시나 좋네요.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-afdb7217-ea86-4c51-92db-426db9751269"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d642cfd-4a37-11f0-b773-799535743876">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-72b9280d-df2a-41d4-99ab-5672419afdd7"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d642cfe-4a37-11f0-b773-b157cf0a2d4c">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-56f429b9-5077-4161-b94b-dc5cd68b537f&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-image se-l-default __se-component" id="SE-4d792398-f3bd-4007-88ab-67621980f665">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-4d792398-f3bd-4007-88ab-67621980f665&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTFfMzYg/MDAxNzQ5NjM3Mzc3OTk5.PiT5mUb25PxZocgXo42BfD_TPI7S9X9pcWpL6GTgK7Eg.fe7UQVwxV7ESL4j9-4C6l8WHyxliXcel3Fayg-j4jE0g.JPEG/20250611_142921.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTFfMzYg/MDAxNzQ5NjM3Mzc3OTk5.PiT5mUb25PxZocgXo42BfD_TPI7S9X9pcWpL6GTgK7Eg.fe7UQVwxV7ESL4j9-4C6l8WHyxliXcel3Fayg-j4jE0g.JPEG/20250611_142921.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-4d792398-f3bd-4007-88ab-67621980f665_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-4d792398-f3bd-4007-88ab-67621980f665&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-80d4c696-4a37-11f0-b773-271aeedb8216">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-a5ee7b3d-d2c9-4e4d-b5ee-edf220cb7289"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d642cff-4a37-11f0-b773-df72e10e4d3b">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-cb26f46c-51cd-4833-b42b-0e5e6be35d10"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d642d00-4a37-11f0-b773-b3ad1605068c">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-55664352-505f-4f77-b45e-d5b8f1017966"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d645411-4a37-11f0-b773-01a6a6e46df7"><b>팔공해물짬뽕(13,000원)</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-6cd4e233-8cb5-45fb-830b-ec84dc766961"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d645412-4a37-11f0-b773-65384b042104">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-550f9edb-3af3-4fbf-abe9-90f28e7e5810"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d645413-4a37-11f0-b773-87cdab81f181">최근래 먹은 해물짬뽕 중에서 해산물이 제일 많이 들어 있다고 해야할까요? 큼직큼직하게 들어 있으면서 묵직한 듯 한게 눈으로만 봐도 '맛있겠구나' 라는 생각이 팍팍 들었습니다.</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-80d4c696-4a37-11f0-b773-271aeedb8216&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-image se-l-default __se-component" id="SE-841af39d-7dad-4ef3-9d33-c508fa58cace">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-841af39d-7dad-4ef3-9d33-c508fa58cace&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTFfMTA3/MDAxNzQ5NjM3Mzc5NDk5.fq_5S1g7i43y_EnBYDJAE8d5UqgGnHRQ_oe10hxhR10g.Z7GvR5Vx9QxHCxuyupUaZ0u5sF6MXSZPs1TzNLwNnsIg.JPEG/20250611_142913.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTFfMTA3/MDAxNzQ5NjM3Mzc5NDk5.fq_5S1g7i43y_EnBYDJAE8d5UqgGnHRQ_oe10hxhR10g.Z7GvR5Vx9QxHCxuyupUaZ0u5sF6MXSZPs1TzNLwNnsIg.JPEG/20250611_142913.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-841af39d-7dad-4ef3-9d33-c508fa58cace_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-841af39d-7dad-4ef3-9d33-c508fa58cace&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-2d2cc2a2-073d-4b52-9ad0-2f9a0fd7fb3e">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-c7a541ab-e318-4fee-972e-823c6726e1a9"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d645414-4a37-11f0-b773-376c59e89837">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-70f19353-4373-431a-80f2-19d93e7cc7ec"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d645415-4a37-11f0-b773-f14921ff7c67">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-b68a0283-94d4-4169-a31b-13d1b886708e"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d645416-4a37-11f0-b773-3bef34a40450">처음 나온 볶음밥은 셋이서 맛나게 먹고 각자의 음식을 탐닉하기 시작합니다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-22520952-632c-4828-987d-6aa58a534a24"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d645417-4a37-11f0-b773-695db10c441e">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-258c304d-408b-496c-8eed-690d007762e3"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d645418-4a37-11f0-b773-257ea55dd282">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-2d2cc2a2-073d-4b52-9ad0-2f9a0fd7fb3e&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-image se-l-default __se-component" id="SE-00dfb4d6-3e4d-4648-a2fb-710fae94bb7f">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-00dfb4d6-3e4d-4648-a2fb-710fae94bb7f&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTFfODcg/MDAxNzQ5NjM3NDAzMzY5.IIt7wi5bX26ZjS-OEIc6a6gBnJGoCiOAzWsW1bRUBU8g.Vb1Eshsetli6fxaC0H3a1KxCM4ET6x0hMx7M3-FRHU8g.JPEG/20250611_142940.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTFfODcg/MDAxNzQ5NjM3NDAzMzY5.IIt7wi5bX26ZjS-OEIc6a6gBnJGoCiOAzWsW1bRUBU8g.Vb1Eshsetli6fxaC0H3a1KxCM4ET6x0hMx7M3-FRHU8g.JPEG/20250611_142940.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-00dfb4d6-3e4d-4648-a2fb-710fae94bb7f_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-00dfb4d6-3e4d-4648-a2fb-710fae94bb7f&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-354103e5-064c-4fad-a751-77c025b785e3">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-55194f8d-acfc-495f-8e80-2a94f1ec4823"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d645419-4a37-11f0-b773-a159bd65adfc">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-44d6decc-7959-4a86-a18f-5f3a1af1d9a2"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d64541a-4a37-11f0-b773-6972e620cf2e">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-200a5cea-3eda-4db0-9ba7-61611f929402"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d64541b-4a37-11f0-b773-e79a630e2702">탱글탱글한 해물들이 어짜피 냉동이겠지만 그래도 싱싱(?)한 듯 맛있습니다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-954c198a-a444-4832-9313-0f74aaa6ed45"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d64541c-4a37-11f0-b773-5783b6db7f90">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-e063dc13-8d57-49ea-8af7-625f3846f52a"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d64541d-4a37-11f0-b773-49ead29d1a59">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-354103e5-064c-4fad-a751-77c025b785e3&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-image se-l-default __se-component" id="SE-990769e3-4a67-42e1-a4ff-608ee04c8a47">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-990769e3-4a67-42e1-a4ff-608ee04c8a47&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTFfMjA2/MDAxNzQ5NjM3Mzk1NTA0.IWK20k2WTLSaSY68PztT2sFCff52QU_9izP-ekOn1m0g.rPQgWfOAJsjU52QoJGZiCioR13L6y83PzwGXkvOuPOcg.JPEG/20250611_142957.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTFfMjA2/MDAxNzQ5NjM3Mzk1NTA0.IWK20k2WTLSaSY68PztT2sFCff52QU_9izP-ekOn1m0g.rPQgWfOAJsjU52QoJGZiCioR13L6y83PzwGXkvOuPOcg.JPEG/20250611_142957.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-990769e3-4a67-42e1-a4ff-608ee04c8a47_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-990769e3-4a67-42e1-a4ff-608ee04c8a47&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-7cf9aed9-ff88-47b7-8db7-96ba06344640">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-cf015ab9-9476-47ed-b4fd-bd909f37f61f"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d64541e-4a37-11f0-b773-fd4a436145ae">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-6ab6b368-9995-4c41-9205-edcda07b0b4f"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d64541f-4a37-11f0-b773-31cbc61fb67c">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-4f1dc8da-06a4-40a1-bbea-cfbec2b77d9e"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d645420-4a37-11f0-b773-6b592b70b643">면발도 좋고 캬~...</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-ac5eb254-8bb2-450b-906b-f22ec8dab95d"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d645421-4a37-11f0-b773-6310424d4792">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-ef758510-806e-4c05-af67-e8f2f85ab1e3"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d645422-4a37-11f0-b773-6973faca9739">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-7cf9aed9-ff88-47b7-8db7-96ba06344640&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-image se-l-default __se-component" id="SE-90deceaa-64a9-4833-95a3-dfe8fe10f7de">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-90deceaa-64a9-4833-95a3-dfe8fe10f7de&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTFfMTYw/MDAxNzQ5NjM3NDAyNzUz.As0b0S_MeO_yeaJIEGmQ4yDjEjW39Y-Dmsc1MqxLF6Ig.aro_ZZymjX_aKqpi9lQYK7Blw8armypFyUTKUon1zcsg.JPEG/20250611_143110.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTFfMTYw/MDAxNzQ5NjM3NDAyNzUz.As0b0S_MeO_yeaJIEGmQ4yDjEjW39Y-Dmsc1MqxLF6Ig.aro_ZZymjX_aKqpi9lQYK7Blw8armypFyUTKUon1zcsg.JPEG/20250611_143110.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-90deceaa-64a9-4833-95a3-dfe8fe10f7de_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-90deceaa-64a9-4833-95a3-dfe8fe10f7de&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-9933ca0f-566f-4194-a13d-1761933fe61d">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-ba0eae51-77e6-4772-a561-140bc1941ba3"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d647b33-4a37-11f0-b773-e336ddb24695">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-785685bc-a8da-458d-b1af-6d34d367f6a0"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d647b34-4a37-11f0-b773-3fda478d51ff">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-5942ea02-4f89-4c27-82c0-cec838a59539"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d647b35-4a37-11f0-b773-9b1d1e436d44">비싼(?)선동오징어도 푸짐하게 들어있네요. 대왕이, 솔방울 이런 거 없습니다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-f9312e94-3106-4dd4-ae79-087dfffc945a"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d647b36-4a37-11f0-b773-896f14c9e68c">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-156e56ab-2401-401a-9aae-01d9e87aaebe"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d647b37-4a37-11f0-b773-85d1f441cb5c">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-9933ca0f-566f-4194-a13d-1761933fe61d&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-image se-l-default __se-component" id="SE-70507629-a3e4-4c7f-a528-f8e3fc6b0e4e">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-70507629-a3e4-4c7f-a528-f8e3fc6b0e4e&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTFfMjQz/MDAxNzQ5NjM3NDg0MTg5.IkWdLSCI7aoUc3G9GwWsZ0Nyi-UrEzVXre1LNhRPJ6Ug.v0q9l0O1pNNxUmWMU0Qbr6aaR8Z5TpKMbSmzZTwmuOog.JPEG/20250611_143107.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTFfMjQz/MDAxNzQ5NjM3NDg0MTg5.IkWdLSCI7aoUc3G9GwWsZ0Nyi-UrEzVXre1LNhRPJ6Ug.v0q9l0O1pNNxUmWMU0Qbr6aaR8Z5TpKMbSmzZTwmuOog.JPEG/20250611_143107.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-70507629-a3e4-4c7f-a528-f8e3fc6b0e4e_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-70507629-a3e4-4c7f-a528-f8e3fc6b0e4e&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-ca21b3fe-0fb4-4df4-a523-22c6085b3112">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-0a6b89cd-52ae-474a-90f4-5a85bb25e565"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d647b38-4a37-11f0-b773-1b08614a0def">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-d64347b0-9a54-4596-a4f9-610862953b08"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d647b39-4a37-11f0-b773-41f3ee63a1d5">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-cc928bb8-424a-49b1-b7ae-14309d63d28f"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d647b3a-4a37-11f0-b773-553b09571167">맛있는 짬뽕은 해산물부터 국물까지 다 맛있습니다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-7ba8da2c-6212-40f2-97ac-c985f42c66b5"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d647b3b-4a37-11f0-b773-cdbbfdab3b0b">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-828d51e6-f7f9-40be-a6b1-c77390708ba1"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d647b3c-4a37-11f0-b773-253aa23e43a7">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-7436e430-9acc-45e3-918f-a820fc8b3a18"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d647b3d-4a37-11f0-b773-adf700d4cecd">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-ca21b3fe-0fb4-4df4-a523-22c6085b3112&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-image se-l-default __se-component" id="SE-1aac9bde-be00-4c7a-ab1f-435ea46c7a24">
                        <div class="se-component-content se-component-content-fit">
                            <div class="se-section se-section-image se-l-default se-section-align-">
                                    <div class="se-module se-module-image" style="">
                                        <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-1aac9bde-be00-4c7a-ab1f-435ea46c7a24&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTFfMTA3/MDAxNzQ5NjQ1NTQ0MTQ3.NJIaI40ZC_0r8ZNlDf8CMZyWijX0-ahMyIur3uxA7KIg.atjhbEqz-3M29_Q7_H7N9uFFsxQeD11ooqKtfuHiWXYg.JPEG/20250611_144625.jpg&quot;, &quot;originalWidth&quot; : &quot;800&quot;, &quot;originalHeight&quot; : &quot;450&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                            <img src="https://postfiles.pstatic.net/MjAyNTA2MTFfMTA3/MDAxNzQ5NjQ1NTQ0MTQ3.NJIaI40ZC_0r8ZNlDf8CMZyWijX0-ahMyIur3uxA7KIg.atjhbEqz-3M29_Q7_H7N9uFFsxQeD11ooqKtfuHiWXYg.JPEG/20250611_144625.jpg?type=w773" data-lazy-src="" data-width="693" data-height="389" alt="" class="se-image-resource egjs-visible" id="SE-1aac9bde-be00-4c7a-ab1f-435ea46c7a24_0">
                                        </a>
                                    </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-1aac9bde-be00-4c7a-ab1f-435ea46c7a24&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-1b3c4175-9741-4378-9b23-356365799d7f">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-79306ca4-56b3-4b6d-9ad8-94eda0f9b1ce"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d647b3e-4a37-11f0-b773-b5023ccaf943">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-2bf57d5d-b6e0-4c23-a979-f648143caf24"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d647b3f-4a37-11f0-b773-41b97390c7a0">줄을 서는 게 무서워서 국물 한방울 안남기고 클리어 했습니다. (국물이 구수하면서 적당히 묵직하고 정말 맛있습니다.)</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-070612a6-047c-41e8-a34b-143a806c9e3f"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d647b40-4a37-11f0-b773-13c42fc6ae81">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-1b3c4175-9741-4378-9b23-356365799d7f&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>                <div class="se-component se-quotation se-l-quotation_underline" id="SE-a7d29c8b-97a2-471e-9bf0-037c94ad1063">
                        <div class="se-component-content">
                            <div class="se-section se-section-quotation se-l-quotation_underline">
                                <blockquote class="se-quotation-container">
                                    <div class="se-module se-module-text se-quote"><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-cdf1f911-8e43-40c7-87ff-14ab5fc2a948"><span style="" class="se-fs- se-ff-   " id="SE-9d647b41-4a37-11f0-b773-05311b2ea081">최종평가: 올해 먹은 짬뽕 중 최고라고 감히 말을 할 수 있을 거 같습니다. 예전보다 더 맛있어 졌으니 사람이 더 많아졌겠죠. 참고로 옛날고기짬뽕은 1시30분전에 솔드아웃된다고 합니다.</span></p><!-- } SE-TEXT --></div>
                                </blockquote>
                            </div>
                        </div>
                    </div>
                    <div class="se-component se-text se-l-default" id="SE-c54634a2-5583-4340-b2a6-eb593294a025">
                        <div class="se-component-content">
                            <div class="se-section se-section-text se-l-default">
                                <div class="se-module se-module-text">
                                        <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-f3ccefae-3521-47a8-82cc-f8a73325a583"><span style="" class="se-fs-fs16 se-ff-nanumbarungothic   " id="SE-9d647b42-4a37-11f0-b773-6fb81a633111">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                </div>
                            </div>
                        </div>
                        <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-c54634a2-5583-4340-b2a6-eb593294a025&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                    </div>    <div class="ssp-adcontent align_center"><div id="ssp-adcontent" class="ssp_adcontent_inner"><div style="width: 100%; height: auto; margin: 0px auto; line-height: 0;"><iframe id="ssp-adcontent_tgtLREC" frameborder="no" scrolling="no" tabindex="0" name="" title="AD" style="width: 100%; height: 211px; visibility: inherit; border: 0px; vertical-align: bottom;"></iframe></div></div></div></div>""",
                "title": "팔공",
                "summary": "중화요리 맛집 홍보"
            },
            {
                "raw_html":
                    """<div class="se-main-container">
                        <div class="se-component se-text se-l-default" id="SE-8972dd43-8d78-4050-ba59-b96fa458e4af">
                            <div class="se-component-content">
                                <div class="se-section se-section-text se-l-default">
                                    <div class="se-module se-module-text">
                                            <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-f68001eb-2efe-4957-bc58-6f6a32d2b447"><span style="" class="se-fs-fs16 se-ff-   " id="SE-2d48c6f0-e323-49c2-b8ca-dc0270215f08">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-58a1b41e-5ff0-49d1-9bf5-83c30ae40c49"><span style="" class="se-fs-fs16 se-ff-   " id="SE-914de671-e763-4a44-9e0f-d25da2fa3fe2">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-4ebb8c16-1f67-4e1e-bd08-65f12868b78e"><span style="" class="se-fs-fs19 se-ff-   " id="SE-b3ff6f9e-8e0b-4a1b-bc31-827d0b6bea98"><b>&ZeroWidthSpace;</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-2dc3e73e-870d-4e27-8695-5a320fa89c6c"><span style="" class="se-fs-fs19 se-ff-   " id="SE-c35ee8ae-d400-4076-abd0-675e205167fe"><b>&ZeroWidthSpace;</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-5c94f24a-737c-4d44-9710-3ac8c8696927"><span style="" class="se-fs-fs19 se-ff-   " id="SE-16b32fe5-44ea-4d4b-b9d0-26d1962792c5"><b>&ZeroWidthSpace;</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-d535c995-f5ce-43f0-8d45-a4d4b286c4a5"><span style="" class="se-fs-fs19 se-ff-   " id="SE-39f0ca51-916e-4f2a-a1b6-60ff5760c28d"><b>[남천동 맛집] 안목 - 훌륭한 돼지국밥 한 그릇</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-24add561-4639-4f0e-bf3d-b94c722b466a"><span style="" class="se-fs-fs19 se-ff-   " id="SE-847c08a8-a8c8-4c0d-a5c0-6243f3d8361b"><b>&ZeroWidthSpace;</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-7a9c4e96-48b1-4d5b-8caa-9ea705f2186c"><span style="" class="se-fs-fs19 se-ff-   " id="SE-11d047cb-30e6-4e69-87c9-a803530e98e8"><b>&ZeroWidthSpace;</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-0030deae-9f55-4917-845d-0f7ae4809b9a"><span style="" class="se-fs-fs19 se-ff-   " id="SE-d4602c8d-7347-4a10-863c-4281f96fe94a"><b>&ZeroWidthSpace;</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-1c5d144a-739f-4f85-93e6-f5d73b834585"><span style="" class="se-fs-fs19 se-ff-   " id="SE-53403223-1e28-4962-bce2-5d35848e168c"><b>&ZeroWidthSpace;</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-07378dbd-5488-41ea-a246-1babecd92954"><span style="" class="se-fs-fs16 se-ff-   " id="SE-db0aff3f-5206-4e81-9214-1d5d10add590">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-e2d99036-8ac7-4faf-b823-4373cc70ccb6"><span style="" class="se-fs-fs16 se-ff-   " id="SE-417853c7-e9a4-4ac1-9fd5-fa40775645a9">미쉐린에 선택한 식당에 특별히 호감이 가는 것은 아니다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-f9ba5875-2292-49a1-99b9-b02ff09ab22a"><span style="" class="se-fs-fs16 se-ff-   " id="SE-68c8a93c-1ca9-4eb0-85f3-da8977ba36fe">하지만 궁금하기는 하다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-ee30d046-dcf4-4171-87bf-b59116c46897"><span style="" class="se-fs-fs16 se-ff-   " id="SE-1d67e180-7206-4946-a2b6-63024a7af26f">어떤 점에서 좋게 보고 선정을 한 것인지 궁금했다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-67f6ee46-1f4f-4b8e-b656-3715305641aa"><span style="" class="se-fs-fs16 se-ff-   " id="SE-05ec4763-389c-40fa-968d-ff653575883e">내가 가본 식당이라면 판단하면 되겠지만 가보지 않은 식당이라면 그 궁금증은 더 크다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-4287a87f-2ba6-43b8-b82b-20a0001a4767"><span style="" class="se-fs-fs16 se-ff-   " id="SE-325e99c2-2da7-4fda-a16e-e2d63679b237">특히 가장 대중적인 음식이라면 더 클 것이다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-531bd062-1a4e-4ee8-8560-81a00093bda4"><span style="" class="se-fs-fs16 se-ff-   " id="SE-c618ee98-64cf-4a8b-a02a-636ba7080110">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-da3f8d8d-f1db-427a-979c-8aebf5958540"><span style="" class="se-fs-fs16 se-ff-   " id="SE-b60789c7-3f22-4fad-89b1-fbd4be75f036">부산의  미쉐린 빕구르망에 2년 연속 선정한 돼지국밥집이 있다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-11ec2577-2f13-4b76-9a98-a173cf683c28"><span style="" class="se-fs-fs16 se-ff-   " id="SE-9d4cebb4-2d7f-4022-8b50-74ebaded61d5">오가며 보기는 했지만 아직 가보진 못했다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-5567796c-e787-4090-9392-9181ee59b90f"><span style="" class="se-fs-fs16 se-ff-   " id="SE-5b988865-e35e-426a-a115-1fbb710ba62b">일부러 찾아가 보았다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-54fac8c2-2c73-4ccf-9575-2c2b4358a43d"><span style="" class="se-fs-fs16 se-ff-   " id="SE-6aa8f486-0425-46c9-a628-124351ee4a33">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-7ffca828-6d76-4770-b6fb-85d812b463cd"><span style="" class="se-fs-fs16 se-ff-   " id="SE-cf804162-ea25-453b-aae3-698ffa027d96">남천동의 "안목"이다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-a6869ff2-5020-4fe8-be9f-400a156859f3"><span style="" class="se-fs-fs16 se-ff-   " id="SE-a3134433-0d3f-48c8-90a8-b05f18971fb9">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-5a4faabf-b052-4fae-8121-5a8388cd3dc0"><span style="" class="se-fs-fs16 se-ff-   " id="SE-144e8c8d-3fb0-4d06-858b-64c3fcd19f14">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                    </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-8972dd43-8d78-4050-ba59-b96fa458e4af&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                        </div>                <div class="se-component se-image se-l-default __se-component" id="SE-82b5ea0a-3a37-4b36-8d8d-d7f08e30ce48">
                            <div class="se-component-content se-component-content-normal">
                                <div class="se-section se-section-image se-l-default se-section-align-" style="max-width:559px;">
                                        <div class="se-module se-module-image" style="">
                                            <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-82b5ea0a-3a37-4b36-8d8d-d7f08e30ce48&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfMjg1/MDAxNzQ5OTY4NTcyNzY2.LGmpZxtuoJiHLxke6n44UwDdAApTtp0zknc7cyAQwMkg.mj4UBfBVnrYE-lBdwGnKvqeOaPffVJRQWhNpCYWOq5gg.JPEG/fec31ed4-4531-40e6-bb29-9a8942380569.jpg&quot;, &quot;originalWidth&quot; : &quot;559&quot;, &quot;originalHeight&quot; : &quot;558&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                                <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfMjg1/MDAxNzQ5OTY4NTcyNzY2.LGmpZxtuoJiHLxke6n44UwDdAApTtp0zknc7cyAQwMkg.mj4UBfBVnrYE-lBdwGnKvqeOaPffVJRQWhNpCYWOq5gg.JPEG/fec31ed4-4531-40e6-bb29-9a8942380569.jpg?type=w966" data-lazy-src="" data-width="559" data-height="558" alt="" class="se-image-resource egjs-visible" id="SE-82b5ea0a-3a37-4b36-8d8d-d7f08e30ce48_0">
                                            </a>
                                        </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-82b5ea0a-3a37-4b36-8d8d-d7f08e30ce48&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                        </div>
                        <div class="se-component se-text se-l-default" id="SE-941b8dd3-032b-41b3-b1e7-de21be4b1ac1">
                            <div class="se-component-content">
                                <div class="se-section se-section-text se-l-default">
                                    <div class="se-module se-module-text">
                                            <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-1239eca6-4dad-4316-b4c2-633e7108a20d"><span style="" class="se-fs-fs16 se-ff-   " id="SE-f8507731-a58b-4336-be5f-51772427c2cc">정문 사진을 찍지 못해서 구글에서 하나 가져왔다. </span><span style="" class="se-fs-fs16 se-ff-   " id="SE-1184468b-6888-47b6-bd79-b25c8fa28ff1">밖에서 봐도 돼지국밥집 같아 보이지 않는다. 깔끔하고 모던하다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-51f3dda1-923d-46cc-b961-b2eb6fa76d1d"><span style="" class="se-fs-fs16 se-ff-   " id="SE-c91360fc-7a03-4f7e-90f3-b13b6ad1ee4f">남천동 등기소 바로 옆 건물이다. 주차장은 별도로 없으니 뒷골목의 주차장을 이용하여야 한다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-eccfaddf-4d21-4fc8-8140-ba636971aec5"><span style="" class="se-fs-fs16 se-ff-   " id="SE-9baa7c62-ba7a-4d0e-b1ed-d29e9eb8ebcf">그런데 상호의 느낌은 일본풍같이 느껴진다. 혹시 그 뜻을 아시는 분들은 좀 알려주시면 고맙겠다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-fdcaf3c0-df33-4cbf-8ee5-dfd972a14a25"><span style="" class="se-fs-fs16 se-ff-   " id="SE-b007c987-1de1-4657-8857-5ec86d451dee">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-70427665-d8e7-4ee6-8ed4-b5d8d88d7f31"><span style="" class="se-fs-fs16 se-ff-   " id="SE-a0d976c5-98e4-41ec-ace4-347ca942dc7a">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-3b35fe66-9f3e-4cad-9c45-976a802173a6"><span style="" class="se-fs-fs16 se-ff-   " id="SE-625d247a-f58e-4b4b-8ddf-d1e57c8ab3ba">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                    </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-941b8dd3-032b-41b3-b1e7-de21be4b1ac1&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                        </div>                <div class="se-component se-image se-l-default __se-component" id="SE-f7276b29-999b-45a7-9159-15056660732e">
                            <div class="se-component-content se-component-content-fit">
                                <div class="se-section se-section-image se-l-default se-section-align-">
                                        <div class="se-module se-module-image" style="">
                                            <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-f7276b29-999b-45a7-9159-15056660732e&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfNjgg/MDAxNzQ5OTUzMTk0NDM5.hO4-CmL-sKEuCDrV5dhYCsnHC4vgJLLtHZ8wKjhVnCQg.dMKk_yT22uEpe1YkXAp8SVKQRF4DZ5_o0u8o1QtuBUIg.JPEG/250613PO-010.jpg&quot;, &quot;originalWidth&quot; : &quot;2600&quot;, &quot;originalHeight&quot; : &quot;1950&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                                <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfNjgg/MDAxNzQ5OTUzMTk0NDM5.hO4-CmL-sKEuCDrV5dhYCsnHC4vgJLLtHZ8wKjhVnCQg.dMKk_yT22uEpe1YkXAp8SVKQRF4DZ5_o0u8o1QtuBUIg.JPEG/250613PO-010.jpg?type=w966" data-lazy-src="" data-width="886" data-height="664" alt="" class="se-image-resource egjs-visible" id="SE-f7276b29-999b-45a7-9159-15056660732e_0">
                                            </a>
                                        </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-f7276b29-999b-45a7-9159-15056660732e&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                        </div>
                        <div class="se-component se-text se-l-default" id="SE-9d6e99ac-15e4-41e7-80c5-b158b70763cc">
                            <div class="se-component-content">
                                <div class="se-section se-section-text se-l-default">
                                    <div class="se-module se-module-text">
                                            <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-8fde3da2-8c82-49f4-a8d6-886d27b8f00a"><span style="" class="se-fs-fs16 se-ff-   " id="SE-c67a616e-4ba2-4d2d-99af-6e414c3b6125">좌석은 테이블은 없고 카운터석으로만 되어 있다. 최근 이름난 돼지국밥집들은 다 이런 식으로 만드는 것 같다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-ba5db589-2ad6-473f-9482-157ac28690e8"><span style="" class="se-fs-fs16 se-ff-   " id="SE-00464b1a-d865-4b96-bc2d-247f6e0c4a62">전에 지나다 줄을 서는 것을 보았는데 이날 비가 와서 그랬는지 한가하다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-ccc192f9-8d6c-4a14-a198-7bfa51ae44a4"><span style="" class="se-fs-fs16 se-ff-   " id="SE-ecfa4f09-0c54-4193-939d-317de862a391">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-07a40d2d-943c-4e27-bf15-2727655cf138"><span style="" class="se-fs-fs16 se-ff-   " id="SE-b1dd6d96-f13e-4a0e-a4c3-9a020eebb18a">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-410f8e82-c2e7-4c24-bd20-29fc8275285a"><span style="" class="se-fs-fs16 se-ff-   " id="SE-dbefe201-bb13-4474-a496-05bf25dbba25">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                    </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-9d6e99ac-15e4-41e7-80c5-b158b70763cc&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                        </div>                <div class="se-component se-image se-l-default __se-component" id="SE-6ddd3ccd-a117-4509-a8e4-48fc503870b3">
                            <div class="se-component-content se-component-content-fit">
                                <div class="se-section se-section-image se-l-default se-section-align-">
                                        <div class="se-module se-module-image" style="">
                                            <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-6ddd3ccd-a117-4509-a8e4-48fc503870b3&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfNDMg/MDAxNzQ5OTUzMTk0NTYx.-KO-tiodP5yffS_QXbKv4b9Au6xqlq6RNgNZYFJ7Rywg.6kHpiJpjPQ8U7ttwrgpIXwbveqaXEPVViWgFvcZK-R4g.JPEG/250613PO-012.jpg&quot;, &quot;originalWidth&quot; : &quot;2600&quot;, &quot;originalHeight&quot; : &quot;1952&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                                <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfNDMg/MDAxNzQ5OTUzMTk0NTYx.-KO-tiodP5yffS_QXbKv4b9Au6xqlq6RNgNZYFJ7Rywg.6kHpiJpjPQ8U7ttwrgpIXwbveqaXEPVViWgFvcZK-R4g.JPEG/250613PO-012.jpg?type=w966" data-lazy-src="" data-width="886" data-height="665" alt="" class="se-image-resource egjs-visible" id="SE-6ddd3ccd-a117-4509-a8e4-48fc503870b3_0">
                                            </a>
                                        </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-6ddd3ccd-a117-4509-a8e4-48fc503870b3&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                        </div>
                        <div class="se-component se-text se-l-default" id="SE-05e3eec1-a84a-446b-8dda-a063c144186b">
                            <div class="se-component-content">
                                <div class="se-section se-section-text se-l-default">
                                    <div class="se-module se-module-text">
                                            <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-0ca1a4a3-ed9f-4129-b0d4-463083ebb789"><span style="" class="se-fs-fs16 se-ff-   " id="SE-310f8b8a-5dbf-4ffe-bf83-a39c1b2bb3af">메뉴가 심플하다. 그냥 돼지국밥에 머릿고기 국밥 정도이다. 수육과 냉제육이 있는데 다음에 가게 되면 먹어보고 싶다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-2faf8c01-7c17-4c6a-80b3-6d6c3d39d04a"><span style="" class="se-fs-fs16 se-ff-   " id="SE-791eb2d9-60ff-4339-8a73-0bca1a10e9ee">가격은 비싸지 않은 것은 아닌데 더 비싸지 않아서 다행스럽다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-9a27fb98-3910-4d9b-9926-7b5e9945a7b1"><span style="" class="se-fs-fs16 se-ff-   " id="SE-1cdbcd49-512c-4050-bc48-e7ee7c95a0de">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-d06d0ae3-90e0-463b-9e9a-72e9a72c20ba"><span style="" class="se-fs-fs16 se-ff-   " id="SE-96f8451c-70a7-4c31-9413-0b4d727ed96d">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-95ab60f8-4221-4cab-913c-8cbc6ead3930"><span style="" class="se-fs-fs16 se-ff-   " id="SE-46eecb93-af1b-42a1-9470-b2f4187ef6cf">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                    </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-05e3eec1-a84a-446b-8dda-a063c144186b&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                        </div>                <div class="ssp-adcontent align_center"><div id="ssp-adcontent-1" class="ssp_adcontent_inner"><div style="width: 100%; height: auto; margin: 0px auto; line-height: 0;"><iframe id="ssp-adcontent-1_tgtLREC" frameborder="no" scrolling="no" tabindex="0" name="" title="AD" style="width: 100%; height: 170px; visibility: inherit; border: 0px; vertical-align: bottom;"></iframe></div></div></div><div class="se-component se-image se-l-default __se-component" id="SE-aa5d8007-954a-4ef4-91c2-3d2b505844a0">
                            <div class="se-component-content se-component-content-fit">
                                <div class="se-section se-section-image se-l-default se-section-align-">
                                        <div class="se-module se-module-image" style="">
                                            <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-aa5d8007-954a-4ef4-91c2-3d2b505844a0&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfMjYw/MDAxNzQ5OTUzMTk0NTk2.UX5VKE-1YZHtzjw6rEpZV257GVxWN0I2v-wHyCTg18Eg.DWrBj9R8C-6izaswmeUv9M6rr0egqauq5YiOFy0NeCYg.JPEG/250613PO-011.jpg&quot;, &quot;originalWidth&quot; : &quot;2600&quot;, &quot;originalHeight&quot; : &quot;1950&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                                <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfMjYw/MDAxNzQ5OTUzMTk0NTk2.UX5VKE-1YZHtzjw6rEpZV257GVxWN0I2v-wHyCTg18Eg.DWrBj9R8C-6izaswmeUv9M6rr0egqauq5YiOFy0NeCYg.JPEG/250613PO-011.jpg?type=w966" data-lazy-src="" data-width="886" data-height="664" alt="" class="se-image-resource egjs-visible" id="SE-aa5d8007-954a-4ef4-91c2-3d2b505844a0_0">
                                            </a>
                                        </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-aa5d8007-954a-4ef4-91c2-3d2b505844a0&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                        </div>
                        <div class="se-component se-text se-l-default" id="SE-f80e8840-2181-4865-82ee-f76852ff8a8d">
                            <div class="se-component-content">
                                <div class="se-section se-section-text se-l-default">
                                    <div class="se-module se-module-text">
                                            <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-2eb9b2d9-40b0-47c8-8f21-281ec86d1d86"><span style="" class="se-fs-fs16 se-ff-   " id="SE-b69fe4e9-1acc-40ea-bc8e-2b9a2ea551f4">첨가할 수 있는 여러 가지</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-b94aa8ae-850e-4358-8ea6-84ef9375df59"><span style="" class="se-fs-fs16 se-ff-   " id="SE-54bcbf91-987e-49da-b535-6e9661cff28f">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-8e838fdb-a7d4-47e1-8c71-0e09ad78b70e"><span style="" class="se-fs-fs16 se-ff-   " id="SE-d924f9a4-7038-47d5-80da-72abfb50a805">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-6dcc38c3-9495-4be7-a260-c62fc0f5a381"><span style="" class="se-fs-fs16 se-ff-   " id="SE-a53e4f33-a43f-4110-a031-4a7facfb5ad1">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                    </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-f80e8840-2181-4865-82ee-f76852ff8a8d&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                        </div>                <div class="se-component se-imageStrip se-imageStrip3 se-l-default __se-component" id="SE-2cbe84d4-620f-40d1-ba7b-512d2c449703">
                            <div class="se-component-content se-component-content-extend">
                                <div class="se-section se-section-imageStrip se-l-default">
                                    <div class="se-imageStrip-container se-imageStrip-col-3">
                                        <div class="se-module se-module-image" style="width:33.33333333333333%;">
                                            <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-8794d901-23f9-4e06-8172-3ea80a94c211&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfNjkg/MDAxNzQ5OTUzMTk1NDM4.mdnPb--Akfk7LwlfL6tJcjn-lPWDkn1LifHjh6xjz3Ag.YpZI0gHuI2Pb4uVYVE203uxhu7v2fI9C86KR0Sz6-Ycg.JPEG/250613PO-017.jpg&quot;, &quot;originalWidth&quot; : &quot;2600&quot;, &quot;originalHeight&quot; : &quot;1952&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                                <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfNjkg/MDAxNzQ5OTUzMTk1NDM4.mdnPb--Akfk7LwlfL6tJcjn-lPWDkn1LifHjh6xjz3Ag.YpZI0gHuI2Pb4uVYVE203uxhu7v2fI9C86KR0Sz6-Ycg.JPEG/250613PO-017.jpg?type=w466" data-lazy-src="" data-width="886" data-height="665" alt="" class="se-image-resource egjs-visible" id="SE-2cbe84d4-620f-40d1-ba7b-512d2c449703_0">
                                            </a>
                                        </div>
                                        <div class="se-module se-module-image" style="width:33.33333333333333%;">
                                            <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-b7c21eec-d1b4-4623-96ec-66889c3f268f&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfMTQw/MDAxNzQ5OTUzMTk1MzM4._F3YiBz5c7ABo1FvDihWT9FT3hScWfhE2_OSnZLGbl4g.eg0JfCaUJLZsdp9AKJ0zk-wCovSCHW1j6Dn4mEmD1A0g.JPEG/250613PO-016.jpg&quot;, &quot;originalWidth&quot; : &quot;2600&quot;, &quot;originalHeight&quot; : &quot;1952&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                                <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfMTQw/MDAxNzQ5OTUzMTk1MzM4._F3YiBz5c7ABo1FvDihWT9FT3hScWfhE2_OSnZLGbl4g.eg0JfCaUJLZsdp9AKJ0zk-wCovSCHW1j6Dn4mEmD1A0g.JPEG/250613PO-016.jpg?type=w466" data-lazy-src="" data-width="886" data-height="665" alt="" class="se-image-resource egjs-visible" id="SE-2cbe84d4-620f-40d1-ba7b-512d2c449703_1">
                                            </a>
                                        </div>
                                        <div class="se-module se-module-image" style="width:33.33333333333333%;">
                                            <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-816c496d-202c-4a23-ac92-dafb9224ef3b&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfODQg/MDAxNzQ5OTUzMTk0NTc3.kOKe2hbU4i3WRZKvVLd2JHC8CY42DeRgJnL0sU8plCYg.mplDs9HslmITyUGpiTy13BRU99sDy_uo_DZzYCmnT_Yg.JPEG/250613PO-015.jpg&quot;, &quot;originalWidth&quot; : &quot;2600&quot;, &quot;originalHeight&quot; : &quot;1952&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                                <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfODQg/MDAxNzQ5OTUzMTk0NTc3.kOKe2hbU4i3WRZKvVLd2JHC8CY42DeRgJnL0sU8plCYg.mplDs9HslmITyUGpiTy13BRU99sDy_uo_DZzYCmnT_Yg.JPEG/250613PO-015.jpg?type=w466" data-lazy-src="" data-width="886" data-height="665" alt="" class="se-image-resource egjs-visible" id="SE-2cbe84d4-620f-40d1-ba7b-512d2c449703_2">
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_imageStrip&quot;, &quot;id&quot;: &quot;SE-2cbe84d4-620f-40d1-ba7b-512d2c449703&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;imageStrip&quot;, &quot;images&quot;: [ {&quot;ctype&quot;: &quot;image&quot;, &quot;id&quot;: &quot;SE-8794d901-23f9-4e06-8172-3ea80a94c211&quot;, &quot;ai&quot;: &quot;false&quot; } , {&quot;ctype&quot;: &quot;image&quot;, &quot;id&quot;: &quot;SE-b7c21eec-d1b4-4623-96ec-66889c3f268f&quot;, &quot;ai&quot;: &quot;false&quot; } , {&quot;ctype&quot;: &quot;image&quot;, &quot;id&quot;: &quot;SE-816c496d-202c-4a23-ac92-dafb9224ef3b&quot;, &quot;ai&quot;: &quot;false&quot; } ] }}"></script>
                        </div>                <div class="se-component se-text se-l-default" id="SE-528276e4-7259-4824-888f-20c3b7b4ccb4">
                            <div class="se-component-content">
                                <div class="se-section se-section-text se-l-default">
                                    <div class="se-module se-module-text">
                                            <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-915165db-c245-41cf-b222-f11784b55c70"><span style="" class="se-fs-fs16 se-ff-   " id="SE-caf8f6bd-7fc0-4883-a34a-6a00ee015907">이런 것들이 있는데 마늘만 넣어 먹었다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-d2fd8a0e-1c8b-4177-8080-fda75da09b3d"><span style="" class="se-fs-fs16 se-ff-   " id="SE-68e676aa-c4de-474b-a545-5d849115cc5f">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-eb7dbbd4-8f3a-46f3-8774-5ead5dd31d7f"><span style="" class="se-fs-fs16 se-ff-   " id="SE-a5317e38-7923-48fd-85f3-99c16797f39b">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-9bdb428d-14bb-4d80-97c6-d58b4b19f9c2"><span style="" class="se-fs-fs16 se-ff-   " id="SE-09f1d33a-cecf-4807-8695-82e3add18611">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                    </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-528276e4-7259-4824-888f-20c3b7b4ccb4&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                        </div>                <div class="se-component se-image se-l-default __se-component" id="SE-36f88a9e-c778-4564-85dd-973b2deee89d">
                            <div class="se-component-content se-component-content-fit">
                                <div class="se-section se-section-image se-l-default se-section-align-">
                                        <div class="se-module se-module-image" style="">
                                            <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-36f88a9e-c778-4564-85dd-973b2deee89d&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfMTA1/MDAxNzQ5OTUzMTk0NjYz.3_BdMcE3KGJ1AM-LBAiNKSs-yD4hyYVEwplaFtuWYywg.ATj_rHsF-0UMu9USJ8Tv63voaon-qtczU6OqAXZ9MwUg.JPEG/250613PO-013.jpg&quot;, &quot;originalWidth&quot; : &quot;2600&quot;, &quot;originalHeight&quot; : &quot;1952&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                                <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfMTA1/MDAxNzQ5OTUzMTk0NjYz.3_BdMcE3KGJ1AM-LBAiNKSs-yD4hyYVEwplaFtuWYywg.ATj_rHsF-0UMu9USJ8Tv63voaon-qtczU6OqAXZ9MwUg.JPEG/250613PO-013.jpg?type=w966" data-lazy-src="" data-width="886" data-height="665" alt="" class="se-image-resource egjs-visible" id="SE-36f88a9e-c778-4564-85dd-973b2deee89d_0">
                                            </a>
                                        </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-36f88a9e-c778-4564-85dd-973b2deee89d&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                        </div>
                        <div class="se-component se-text se-l-default" id="SE-c44978b7-eb24-4446-8a16-a3bd6f82e5bb">
                            <div class="se-component-content">
                                <div class="se-section se-section-text se-l-default">
                                    <div class="se-module se-module-text">
                                            <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-ff7ae63d-d559-45fe-95bd-ce1fa6888ec9"><span style="" class="se-fs-fs16 se-ff-   " id="SE-b3d8985d-0a55-43c2-844f-1a5b5f8093d2">내가 주문한 머릿고기 국밥이다. 1인분씩 담겨 나온다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-b8da85d8-c54c-46ff-9c1f-03fc0efc6b27"><span style="" class="se-fs-fs16 se-ff-   " id="SE-fb2569cc-5596-47ee-b4a5-61b85577966a">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-e26f989f-7d90-4677-878e-9c80231b5312"><span style="" class="se-fs-fs16 se-ff-   " id="SE-1759c29e-c1d2-4b14-90e5-7bf1d9cb9521">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-8aad23a1-6550-4932-a3e8-f7d94e32aec6"><span style="" class="se-fs-fs16 se-ff-   " id="SE-d90d1aa3-b62b-4a31-b366-31531ed48f02">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                    </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-c44978b7-eb24-4446-8a16-a3bd6f82e5bb&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                        </div>                <div class="se-component se-imageStrip se-imageStrip3 se-l-default __se-component" id="SE-5fcc7790-56b3-42c7-9843-dc22adb55c07">
                            <div class="se-component-content se-component-content-extend">
                                <div class="se-section se-section-imageStrip se-l-default">
                                    <div class="se-imageStrip-container se-imageStrip-col-3">
                                        <div class="se-module se-module-image" style="width:33.33333333333333%;">
                                            <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-aa6e4f52-44e3-42e8-95f9-4ca0353d9ccb&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfMTgy/MDAxNzQ5OTUzMTk2NDU4.LsmyXSqZWwOzW7dy_LzEBGua5jWQCZS9bJoTeEtS53Eg.9I22CI0V0WfM1pXH-MDVKoKwUv5DyCZZZBSCm7mV8oMg.JPEG/250613PO-024.jpg&quot;, &quot;originalWidth&quot; : &quot;2600&quot;, &quot;originalHeight&quot; : &quot;1952&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                                <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfMTgy/MDAxNzQ5OTUzMTk2NDU4.LsmyXSqZWwOzW7dy_LzEBGua5jWQCZS9bJoTeEtS53Eg.9I22CI0V0WfM1pXH-MDVKoKwUv5DyCZZZBSCm7mV8oMg.JPEG/250613PO-024.jpg?type=w466" data-lazy-src="" data-width="886" data-height="665" alt="" class="se-image-resource egjs-visible" id="SE-5fcc7790-56b3-42c7-9843-dc22adb55c07_0">
                                            </a>
                                        </div>
                                        <div class="se-module se-module-image" style="width:33.33333333333333%;">
                                            <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-86620c51-7a6b-443a-b6e1-33eb838caca3&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfMTAw/MDAxNzQ5OTUzMTk1NzUz.WTnw7m2sHlYqhm-gGpDAYDupzgE90NK7-PrxIfAGVcsg.WAHSP9BvkDhrp6ncyd5sLy4sL_5T16fgIildPRzOOW8g.JPEG/250613PO-019.jpg&quot;, &quot;originalWidth&quot; : &quot;2600&quot;, &quot;originalHeight&quot; : &quot;1952&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                                <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfMTAw/MDAxNzQ5OTUzMTk1NzUz.WTnw7m2sHlYqhm-gGpDAYDupzgE90NK7-PrxIfAGVcsg.WAHSP9BvkDhrp6ncyd5sLy4sL_5T16fgIildPRzOOW8g.JPEG/250613PO-019.jpg?type=w466" data-lazy-src="" data-width="886" data-height="665" alt="" class="se-image-resource egjs-visible" id="SE-5fcc7790-56b3-42c7-9843-dc22adb55c07_1">
                                            </a>
                                        </div>
                                        <div class="se-module se-module-image" style="width:33.33333333333333%;">
                                            <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-17fc85ed-1be1-45de-8316-56446d32578f&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfMjQx/MDAxNzQ5OTUzMTk1Nzkx.a0By-nIqlIQDTeCvskwfEPe2e89fAur5V5BK1tBPmkQg.UbhToOdVay9Jht3rKOufMOCRufr_VVRv9907ij0_o-4g.JPEG/250613PO-020.jpg&quot;, &quot;originalWidth&quot; : &quot;2600&quot;, &quot;originalHeight&quot; : &quot;1952&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                                <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfMjQx/MDAxNzQ5OTUzMTk1Nzkx.a0By-nIqlIQDTeCvskwfEPe2e89fAur5V5BK1tBPmkQg.UbhToOdVay9Jht3rKOufMOCRufr_VVRv9907ij0_o-4g.JPEG/250613PO-020.jpg?type=w466" data-lazy-src="" data-width="886" data-height="665" alt="" class="se-image-resource egjs-visible" id="SE-5fcc7790-56b3-42c7-9843-dc22adb55c07_2">
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_imageStrip&quot;, &quot;id&quot;: &quot;SE-5fcc7790-56b3-42c7-9843-dc22adb55c07&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;imageStrip&quot;, &quot;images&quot;: [ {&quot;ctype&quot;: &quot;image&quot;, &quot;id&quot;: &quot;SE-aa6e4f52-44e3-42e8-95f9-4ca0353d9ccb&quot;, &quot;ai&quot;: &quot;false&quot; } , {&quot;ctype&quot;: &quot;image&quot;, &quot;id&quot;: &quot;SE-86620c51-7a6b-443a-b6e1-33eb838caca3&quot;, &quot;ai&quot;: &quot;false&quot; } , {&quot;ctype&quot;: &quot;image&quot;, &quot;id&quot;: &quot;SE-17fc85ed-1be1-45de-8316-56446d32578f&quot;, &quot;ai&quot;: &quot;false&quot; } ] }}"></script>
                        </div>                <div class="se-component se-text se-l-default" id="SE-f6616679-da4e-4eed-a2c6-f9fb36ec3405">
                            <div class="se-component-content">
                                <div class="se-section se-section-text se-l-default">
                                    <div class="se-module se-module-text">
                                            <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-446fc501-5e08-4abb-a3f2-ecad45fea3e6"><span style="" class="se-fs-fs16 se-ff-   " id="SE-180c50c3-fc65-458d-a9db-888422cfa980">머리 위의 선반에 쟁반이 올려져 있으면 그것을 내가 받아서 먹어야 한다. 반찬은 특별한 것은 없는데 이날 풋고추가 맛있었다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-344413c7-d4d6-40a4-b79a-c885d964418a"><span style="" class="se-fs-fs16 se-ff-   " id="SE-d05856f6-f85f-4fbb-a221-e168ce97737f">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-e059cbaf-044c-4d9b-973a-4ad3f9b3ce2d"><span style="" class="se-fs-fs16 se-ff-   " id="SE-5b8941db-4354-48b8-bcc0-37ec82cdff2c">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-fd387d49-e486-48e4-a64f-e5cfa1d1e069"><span style="" class="se-fs-fs16 se-ff-   " id="SE-8f3f9753-04a0-4af1-a45f-fe81c89649ce">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                    </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-f6616679-da4e-4eed-a2c6-f9fb36ec3405&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                        </div>                <div class="se-component se-image se-l-default __se-component" id="SE-ec2a2dd1-f1ce-4c80-943f-7a51d6f5f42a">
                            <div class="se-component-content se-component-content-fit">
                                <div class="se-section se-section-image se-l-default se-section-align-">
                                        <div class="se-module se-module-image" style="">
                                            <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-ec2a2dd1-f1ce-4c80-943f-7a51d6f5f42a&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfNTgg/MDAxNzQ5OTUzMTk1OTU4.0vqNAZDCI3_DgMYJt68O11Qy_SfbkGS-vQ_y8HBvMJsg.KyEtbdEJTDDHKkegTyZGXCIVOY_TiM6gLYTFCDyneTkg.JPEG/250613PO-021.jpg&quot;, &quot;originalWidth&quot; : &quot;2600&quot;, &quot;originalHeight&quot; : &quot;1952&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                                <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfNTgg/MDAxNzQ5OTUzMTk1OTU4.0vqNAZDCI3_DgMYJt68O11Qy_SfbkGS-vQ_y8HBvMJsg.KyEtbdEJTDDHKkegTyZGXCIVOY_TiM6gLYTFCDyneTkg.JPEG/250613PO-021.jpg?type=w966" alt="" class="se-image-resource egjs-visible" id="SE-ec2a2dd1-f1ce-4c80-943f-7a51d6f5f42a_0">
                                            </a>
                                        </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-ec2a2dd1-f1ce-4c80-943f-7a51d6f5f42a&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                        </div>
                        <div class="se-component se-text se-l-default" id="SE-1361609e-ccac-49e3-bc13-dcc6e0604458">
                            <div class="se-component-content">
                                <div class="se-section se-section-text se-l-default">
                                    <div class="se-module se-module-text">
                                            <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-a11430b3-9a84-4f8e-b09c-bdf1854c5835"><span style="" class="se-fs-fs16 se-ff-   " id="SE-38b2e2d5-af70-4466-9b13-39582edf6d97">굉장히 뽀얀 국물의 국밥이다. 머릿고기가 올려져 있다. </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-da8cea63-1841-4a2e-b09e-712965c1e00c"><span style="" class="se-fs-fs16 se-ff-   " id="SE-988e8adc-2db3-474b-995c-d8257bd9a67a">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-966edbce-a062-4865-b16f-891c7665aa57"><span style="" class="se-fs-fs16 se-ff-   " id="SE-356d6f0c-8438-4f31-ae49-fb3875b1f8ca">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-516d6f1f-abda-4392-b853-86f58b689a72"><span style="" class="se-fs-fs16 se-ff-   " id="SE-95150272-61b2-42f4-a1ac-2b19513b5453">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                    </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-1361609e-ccac-49e3-bc13-dcc6e0604458&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                        </div>                <div class="ssp-adcontent align_center"><div id="ssp-adcontent-2" class="ssp_adcontent_inner"><div style="width: 100%; height: auto; margin: 0px auto; line-height: 0;"><iframe id="ssp-adcontent-2_tgtLREC" frameborder="no" scrolling="no" tabindex="0" name="" title="AD" style="width: 100%; height: 170px; visibility: inherit; border: 0px; vertical-align: bottom;"></iframe></div></div></div><div class="se-component se-image se-l-default __se-component" id="SE-f50dd863-0ba5-468e-8d32-c7b635b1e24c">
                            <div class="se-component-content se-component-content-fit">
                                <div class="se-section se-section-image se-l-default se-section-align-">
                                        <div class="se-module se-module-image" style="">
                                            <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-f50dd863-0ba5-468e-8d32-c7b635b1e24c&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfMjIx/MDAxNzQ5OTUzMTk0NTYz.Lez-e3Oz-o3I71zOgsRy0AMh1QSrrvgui5JJkKcoc2Yg.qeKtqLvCOroYFpRZvDfAc8UPXzeXYkZNf4slR0prLb8g.JPEG/250613PO-014.jpg&quot;, &quot;originalWidth&quot; : &quot;2600&quot;, &quot;originalHeight&quot; : &quot;1952&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                                <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfMjIx/MDAxNzQ5OTUzMTk0NTYz.Lez-e3Oz-o3I71zOgsRy0AMh1QSrrvgui5JJkKcoc2Yg.qeKtqLvCOroYFpRZvDfAc8UPXzeXYkZNf4slR0prLb8g.JPEG/250613PO-014.jpg?type=w966" data-lazy-src="" data-width="886" data-height="665" alt="" class="se-image-resource egjs-visible" id="SE-f50dd863-0ba5-468e-8d32-c7b635b1e24c_0">
                                            </a>
                                        </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-f50dd863-0ba5-468e-8d32-c7b635b1e24c&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                        </div>
                        <div class="se-component se-text se-l-default" id="SE-d92a9cee-ed30-433b-a86a-f3abcbd91e86">
                            <div class="se-component-content">
                                <div class="se-section se-section-text se-l-default">
                                    <div class="se-module se-module-text">
                                            <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-56b2cf03-b763-49f5-8168-d79f3a964cce"><span style="" class="se-fs-fs16 se-ff-   " id="SE-5f097fcf-bb48-4f3f-bdee-02e3e49d26f7">이것은 아내가 먹은 그냥 돼지국밥이다. 고기만 다른 국밥이다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-c49d36d8-316d-486a-a3b9-043207a63d79"><span style="" class="se-fs-fs16 se-ff-   " id="SE-31c70de2-2e6a-4ad7-bfff-c3ad81fa1ff4">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-f6413314-198b-45ce-80f2-911121bec20d"><span style="" class="se-fs-fs16 se-ff-   " id="SE-cd08affb-987a-46ea-9b38-915d750a9dee">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-60fdf094-69f4-41bd-a1c7-55c320a6fa91"><span style="" class="se-fs-fs16 se-ff-   " id="SE-8ed25cc9-0962-4792-b252-13c4b4146c9c">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                    </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-d92a9cee-ed30-433b-a86a-f3abcbd91e86&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                        </div>                <div class="se-component se-image se-l-default __se-component" id="SE-1b0c1730-c329-49e3-b6a7-f5e3e3059d0d">
                            <div class="se-component-content se-component-content-fit">
                                <div class="se-section se-section-image se-l-default se-section-align-">
                                        <div class="se-module se-module-image" style="">
                                            <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-1b0c1730-c329-49e3-b6a7-f5e3e3059d0d&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfOTAg/MDAxNzQ5OTUzMTk2MTgy.gVkPsAtlT_KYRAsdDrpHl8PV3r99tOJC4FiHaY0_Y38g.iRRZOD3JywDU20UBT13JgDjLiWbVo5A1pns7JwHDLcEg.JPEG/250613PO-022.jpg&quot;, &quot;originalWidth&quot; : &quot;2600&quot;, &quot;originalHeight&quot; : &quot;1952&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                                <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfOTAg/MDAxNzQ5OTUzMTk2MTgy.gVkPsAtlT_KYRAsdDrpHl8PV3r99tOJC4FiHaY0_Y38g.iRRZOD3JywDU20UBT13JgDjLiWbVo5A1pns7JwHDLcEg.JPEG/250613PO-022.jpg?type=w966" data-lazy-src="" data-width="886" data-height="665" alt="" class="se-image-resource egjs-visible" id="SE-1b0c1730-c329-49e3-b6a7-f5e3e3059d0d_0">
                                            </a>
                                        </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-1b0c1730-c329-49e3-b6a7-f5e3e3059d0d&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                        </div>
                        <div class="se-component se-text se-l-default" id="SE-2b85910d-f5cf-44d5-935b-877dd851be13">
                            <div class="se-component-content">
                                <div class="se-section se-section-text se-l-default">
                                    <div class="se-module se-module-text">
                                            <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-879c344a-a9b8-481b-b211-3c246ec6d786"><span style="" class="se-fs-fs16 se-ff-   " id="SE-05759924-611c-4ab6-a348-34943d45a7f0">국밥에는 간이 되어 있어서 더 넣지 않아도 충분히 먹을 수 있었다. 그러니 다진 양념이나 새우젓은 맛을 보고 첨가하시길....</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-9737e0c9-4372-46a2-8413-cc9268418231"><span style="" class="se-fs-fs16 se-ff-   " id="SE-25d91d40-fce2-4710-bbb7-8465595df438">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-e8e7d092-25b2-471d-bb0c-007a4582e464"><span style="" class="se-fs-fs16 se-ff-   " id="SE-3a58ed48-4aac-4835-86cf-1c86419c03bb">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-abdb29ce-9ceb-498e-a2dc-26223ddeee27"><span style="" class="se-fs-fs16 se-ff-   " id="SE-f5438c07-50cf-44a0-a548-58950d6e6f7c">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                    </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-2b85910d-f5cf-44d5-935b-877dd851be13&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                        </div>                <div class="se-component se-image se-l-default __se-component" id="SE-d6a348f7-f695-43e4-8511-96a3245f87d2">
                            <div class="se-component-content se-component-content-fit">
                                <div class="se-section se-section-image se-l-default se-section-align-">
                                        <div class="se-module se-module-image" style="">
                                            <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-d6a348f7-f695-43e4-8511-96a3245f87d2&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfNDUg/MDAxNzQ5OTUzMTk2NDk4.STY7VWu2civtBUfeFtK9_2pz8sleeohvlYxsVP0HNOQg.4yo-k3SylBh1_t8fxtukLc8RWFB98tkGkYN4VcRups0g.JPEG/250613PO-023.jpg&quot;, &quot;originalWidth&quot; : &quot;2600&quot;, &quot;originalHeight&quot; : &quot;1952&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                                <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfNDUg/MDAxNzQ5OTUzMTk2NDk4.STY7VWu2civtBUfeFtK9_2pz8sleeohvlYxsVP0HNOQg.4yo-k3SylBh1_t8fxtukLc8RWFB98tkGkYN4VcRups0g.JPEG/250613PO-023.jpg?type=w966" data-lazy-src="" data-width="886" data-height="665" alt="" class="se-image-resource egjs-visible" id="SE-d6a348f7-f695-43e4-8511-96a3245f87d2_0">
                                            </a>
                                        </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-d6a348f7-f695-43e4-8511-96a3245f87d2&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                        </div>
                        <div class="se-component se-text se-l-default" id="SE-8156ae0a-1f1b-447a-9889-0cb607d0ce6b">
                            <div class="se-component-content">
                                <div class="se-section se-section-text se-l-default">
                                    <div class="se-module se-module-text">
                                            <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-fc43aeab-ffe3-4ff9-9422-a710bb69d21b"><span style="" class="se-fs-fs16 se-ff-   " id="SE-0c546c1c-1935-41d6-b390-d04c0b28000c">일본 라멘에 넣는 마늘을 짜서 넣는다. 하나 정도면 충분하겠다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-f4cb80dd-35b5-4faa-b8ef-e4eaba82876f"><span style="" class="se-fs-fs16 se-ff-   " id="SE-fb4af1c1-bcf9-4349-8743-97b114d630be">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-a1233be2-5976-4211-ac76-ff4922754a78"><span style="" class="se-fs-fs16 se-ff-   " id="SE-3451db9d-baff-4dd1-a58b-127c5644dca6">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-eee4fc54-5560-4c72-976e-acb0aee1f36f"><span style="" class="se-fs-fs16 se-ff-   " id="SE-a215cb8b-cf4b-4b7c-8bd6-92b875cb4101">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                    </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-8156ae0a-1f1b-447a-9889-0cb607d0ce6b&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                        </div>                <div class="se-component se-image se-l-default __se-component" id="SE-0e6c3ef3-753d-4f44-9920-cccd40d9fe1e">
                            <div class="se-component-content se-component-content-fit">
                                <div class="se-section se-section-image se-l-default se-section-align-">
                                        <div class="se-module se-module-image" style="">
                                            <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-0e6c3ef3-753d-4f44-9920-cccd40d9fe1e&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTVfMTMx/MDAxNzQ5OTUzMTk2ODYw.M5o7UVzbaYgX7j1tU0Z1gcmJ8DsZHXjw-zPXnA6Hu9sg.x4gZfj49wYwPYgWY8V-kufA4k51LkMxYDnmwyFi7GM0g.JPEG/250613PO-025.jpg&quot;, &quot;originalWidth&quot; : &quot;2600&quot;, &quot;originalHeight&quot; : &quot;1952&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                                <img src="https://postfiles.pstatic.net/MjAyNTA2MTVfMTMx/MDAxNzQ5OTUzMTk2ODYw.M5o7UVzbaYgX7j1tU0Z1gcmJ8DsZHXjw-zPXnA6Hu9sg.x4gZfj49wYwPYgWY8V-kufA4k51LkMxYDnmwyFi7GM0g.JPEG/250613PO-025.jpg?type=w966" data-lazy-src="" data-width="886" data-height="665" alt="" class="se-image-resource egjs-visible" id="SE-0e6c3ef3-753d-4f44-9920-cccd40d9fe1e_0">
                                            </a>
                                        </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-0e6c3ef3-753d-4f44-9920-cccd40d9fe1e&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot;, &quot;ai&quot;: &quot;false&quot; }}"></script>
                        </div>
                        <div class="se-component se-text se-l-default" id="SE-ae3b545b-2f63-4ef8-845d-a6ebb23a4dd6">
                            <div class="se-component-content">
                                <div class="se-section se-section-text se-l-default">
                                    <div class="se-module se-module-text">
                                            <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-1f480568-2fbe-402c-899c-8c479fe3f69b"><span style="" class="se-fs-fs16 se-ff-   " id="SE-3cb08f25-f12d-4aed-94bc-765cd4efc26d">맛있게 잘 먹었다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-3882eb95-6212-4ee1-9380-63f19911d467"><span style="" class="se-fs-fs16 se-ff-   " id="SE-0baef1d1-159d-4199-a1cf-ddd44d1eceee">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-ea21710f-65aa-4a76-ba43-509e015fcecf"><span style="" class="se-fs-fs16 se-ff-   " id="SE-5e93172b-b80b-4eb3-9ddb-1374bc49d327">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-1949d40e-ad8f-4c64-b78b-85e4fc46b5af"><span style="" class="se-fs-fs16 se-ff-   " id="SE-919f7a7a-fb30-46c7-82f9-7078b53f7dff">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-6582b269-6321-4315-b4b3-a7187b26a6ba"><span style="" class="se-fs-fs16 se-ff-   " id="SE-8af1132d-ea83-4cc0-8691-ccf3e7f9a7c6">맛있다. 쵸 근래 너무 저가의 돼지국밥만 먹고 다녀서인지 안목의 국밥은 맛있었다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-aef031f5-a9bf-4c89-8ec8-249162baaa9e"><span style="" class="se-fs-fs16 se-ff-   " id="SE-3f0d20b1-6087-4a1f-8065-0c2af54ed3b9">국물이 너무 무겁지도 않으면서도 진득했다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-2868a3e9-a0da-4ad6-8b48-d0610aa61cd7"><span style="" class="se-fs-fs16 se-ff-   " id="SE-964bde86-c8be-4254-907a-e1fc1eed86a4">완성도가 높다. 국물은 손가락에 꼽을 정도로 괜찮았다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-0b638273-7eca-43cc-b1a1-9e9ef0ce2e94"><span style="" class="se-fs-fs16 se-ff-   " id="SE-df79cd06-1dd3-4d42-9cbe-9b52e82491de">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-5f6620d6-8c42-4498-962f-7b6f56ee56fd"><span style="" class="se-fs-fs16 se-ff-   " id="SE-e9d67537-c85d-475a-bcb2-4596aee46e4a">고기의 품질도 좋았고 손질도 잘했다. 부드럽고 또 비계 부분은 쫄깃했다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-14d65629-3ff1-4b91-9ee6-5393b2aea5d9"><span style="" class="se-fs-fs16 se-ff-   " id="SE-97fbd5b2-6ee3-468e-939e-f1a13f3b4eb4">다만 고기가 많아 보이지만 한 점 한 점이 굉장히 얇아서 무게로 치면 그렇게 많은 양은 아닐 것이다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-ae21c386-a521-4952-80f0-4074ecb51e41"><span style="" class="se-fs-fs16 se-ff-   " id="SE-f6c063db-f345-4193-ace3-08c657cef4c1">그리고 국밥 전체적으로 양은 그다지 많은 편은 아니다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-13f5cb93-34b7-49e3-b2c5-3f7abf8c1197"><span style="" class="se-fs-fs16 se-ff-   " id="SE-41556eda-a5d3-44df-bec3-bbe7b86e5cc2">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-17734b9f-8807-4845-bc21-9bd3d57d7315"><span style="" class="se-fs-fs16 se-ff-   " id="SE-36a33986-1c67-4360-8a70-9389dd0b79cd">이 정도의 맛이면 미쉐린 빕구르망에 선정되는 것인지는 모르겠지만 나로서는 충분하다고 느껴진다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-abf04f43-a45b-4277-81d6-ea42f27d3d10"><span style="" class="se-fs-fs16 se-ff-   " id="SE-db758d57-3f3b-4b24-bc71-eeda83b08453">내가 추구하는 수더분하고 푸짐한 국밥하고는 반대편에 있는 국밥이지만 완성도가 높으니 다 괜찮아 보인다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-741083b3-6756-4435-868c-8905ed84d3cf"><span style="" class="se-fs-fs16 se-ff-   " id="SE-ef1cc8f0-ad10-44fa-a0e1-2825034df2e4">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-f05340c7-520a-452a-ad71-b6585d8a0c2a"><span style="" class="se-fs-fs16 se-ff-   " id="SE-028bf6f3-9191-45a0-9302-891e1ad24376">좀 편하게 갈 수 있다면 가끔 가고 싶다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-2a730974-4cee-4a6d-a01f-2610fee6eebc"><span style="" class="se-fs-fs16 se-ff-   " id="SE-bfcadc9a-4d80-469b-a41f-93fdee2b9552">서면과 부산역에 분점이 있다고 하니 그곳이 좀 편하겠다.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-acdccbaa-73b7-4cc8-9921-fb0c9940fd75"><span style="" class="se-fs-fs16 se-ff-   " id="SE-72efa448-1a66-4a29-97cc-600ef01dd020">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-ae1c8bf7-cbdb-4dbe-9d47-117babefd882"><span style="" class="se-fs-fs16 se-ff-   " id="SE-c7f762ec-9db0-4fc1-a463-5bfa4c8c5b43">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-03fae9c9-37ab-4d57-a09d-6fc9438c05f8"><span style="" class="se-fs-fs16 se-ff-   " id="SE-df7f1559-397d-41a4-9116-c9edf83c2210">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-747f981d-de9b-47f9-a1fe-cf2336f6a914"><span style="" class="se-fs-fs16 se-ff-   " id="SE-5a2bc21e-7f0c-4077-8c91-2fbec3cd6fc2">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                    </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-ae3b545b-2f63-4ef8-845d-a6ebb23a4dd6&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                        </div>                <div class="se-component se-placesMap se-l-default __se-component" id="SE-c94683a8-9f85-495a-b23b-88cb68e1e261">
                            <div class="se-component-content">
                                <div class="se-section se-section-placesMap  se-section-align- se-l-default">
                                    <div class="se-module se-module-map-image" style="padding-top: 45%;"><div class="__se_map se-dynamic-map" tabindex="0" style="position: relative; overflow: hidden; background: rgb(248, 249, 250);"><div style="position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; overflow: visible; width: 100%; height: 100%; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); z-index: 0; cursor: url(&quot;https://ssl.pstatic.net/static/maps/mantle/2x/openhand.cur&quot;), default;"><div style="position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; overflow: visible; width: 100%; height: 100%; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); z-index: 0;"><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 1;"><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: none; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 0; user-select: none;"></div><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 1; user-select: none;"><div style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 0px; height: 0px; overflow: visible; box-sizing: content-box !important;"><div draggable="false" unselectable="on" style="position: absolute; top: 242px; left: 246px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112543/51853@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -14px; left: 246px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112543/51852@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 498px; left: 246px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112543/51854@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -270px; left: 246px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112543/51851@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -270px; left: 502px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112544/51851@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 498px; left: -10px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112542/51854@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -14px; left: 502px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112544/51852@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 242px; left: -10px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112542/51853@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 242px; left: 502px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112544/51853@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -14px; left: -10px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112542/51852@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 498px; left: 502px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112544/51854@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -270px; left: -10px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112542/51851@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -270px; left: 758px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112545/51851@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 498px; left: -266px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112541/51854@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -14px; left: 758px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112545/51852@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 242px; left: -266px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112541/51853@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 242px; left: 758px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112545/51853@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -14px; left: -266px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112541/51852@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 498px; left: 758px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112545/51854@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -270px; left: -266px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/112541/51851@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div></div></div><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 100;"><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 101;"></div><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 103;"><div title="" style="position: absolute; overflow: hidden; box-sizing: content-box !important; cursor: inherit; left: 426px; top: 159px; width: 32px; height: 42px;"><img draggable="false" unselectable="on" src="https://editor-static.pstatic.net/c/resources/common/img/common-icon-places-marker-x2-20180920.png" alt="" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; position: absolute; cursor: pointer; width: 32px; height: 42px; left: 0px; top: 0px;"></div></div><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 106;"></div></div></div><div style="position: absolute; display: none; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; overflow: visible; width: 100%; height: 100%; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); background-color: rgb(255, 255, 255); z-index: 10000; opacity: 0.5;"></div></div></div><div style="position: absolute; z-index: 100; margin: 0px; padding: 0px; pointer-events: none; bottom: 0px; right: 0px;"><div style="border: 0px none; margin: 0px; padding: 0px; pointer-events: none; float: right; height: 20px;"><div style="position: relative; width: 51px; height: 14px; margin: 0px 12px 6px 2px; overflow: hidden; pointer-events: auto;"><span style="display: block; margin: 0px; padding: 0px 4px; text-align: center; font-size: 10px; line-height: 11px; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; font-weight: 700; color: rgb(34, 34, 37); text-shadow: rgba(255, 255, 255, 0.8) -1px 0px, rgba(255, 255, 255, 0.8) 0px 1px, rgba(255, 255, 255, 0.8) 1px 0px, rgba(255, 255, 255, 0.8) 0px -1px;">50m</span><img src="https://ssl.pstatic.net/static/maps/mantle/2x/new-scale-normal-b.png" width="45" height="3" alt="" style="position: absolute; left: 3px; bottom: 0px; z-index: 2; display: block; width: 45px; height: 3px; overflow: hidden; margin: 0px; padding: 0px; border: 0px none; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/new-scale-normal-l.png" width="3" height="8" alt="" style="position:absolute;left:0;bottom:0;z-index:2;display:block;width:3px;height:8px;overflow:hidden;margin:0;padding:0;border:0 none;max-width:none !important;max-height:none !important;min-width:0 !important;min-height:0 !important;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/new-scale-normal-r.png" width="3" height="8" alt="" style="position:absolute;right:0;bottom:0;z-index:2;display:block;width:3px;height:8px;overflow:hidden;margin:0;padding:0;border:0 none;max-width:none !important;max-height:none !important;min-width:0 !important;min-height:0 !important;"></div></div></div><div style="position: absolute; z-index: 100; margin: 0px; padding: 0px; pointer-events: none; bottom: 0px; left: 0px;"><div style="border: 0px none; margin: 0px; padding: 0px; pointer-events: none; float: left; height: 21px;"><div class="map_copyright" style="margin: 0px; padding: 0px 0px 2px 10px; height: 19px; line-height: 19px; color: rgb(68, 68, 68); font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; font-size: 11px; clear: both; white-space: nowrap; pointer-events: none;"><div style="float: left;"><span style="white-space: pre; color: rgb(68, 68, 68);">© NAVER Corp.</span></div><a href="#" style="font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; font-size: 11px; line-height: 19px; margin: 0px 0px 0px 5px; padding: 0px; color: rgb(68, 68, 68); float: left; pointer-events: auto; text-decoration: underline; display: none;">더보기</a><div style="float: left;"><a target="_blank" href="http://www.openstreetmap.org/copyright" style="pointer-events: auto; white-space: pre; display: none; color: rgb(68, 68, 68);"> /OpenStreetMap</a></div></div></div></div><div style="border: 1px solid rgb(41, 41, 48); background: rgb(255, 255, 255); padding: 15px; color: rgb(51, 51, 51); position: absolute; font-size: 11px; line-height: 1.5; clear: both; display: none; max-width: 350px !important; max-height: 300px !important;"><h5 style="font-size: 12px; margin-top: 0px; margin-bottom: 10px;">지도 데이터</h5><a href="#" style="position: absolute; top: 8px; right: 8px; width: 14px; height: 14px; font-size: 14px; line-height: 14px; display: block; overflow: hidden; color: rgb(68, 68, 68); text-decoration: none; font-weight: bold; text-align: center;">x</a><div><span style="white-space: pre; color: rgb(68, 68, 68); float: left;">© NAVER Corp.</span><a target="_blank" href="http://www.openstreetmap.org/copyright" style="pointer-events: auto; white-space: pre; color: rgb(68, 68, 68); float: left; display: none;"> /OpenStreetMap</a></div></div><div style="position: absolute; z-index: 100; margin: 0px; padding: 0px; pointer-events: none; top: 0px; right: 0px;"><div style="border: 0px none; margin: 0px; padding: 0px; pointer-events: none; float: right;"><div style="position: relative; z-index: 3; pointer-events: auto;"><div style="position: relative; z-index: 0; width: 28px; margin: 10px; border: 1px solid rgb(68, 68, 68); box-sizing: content-box !important; user-select: none;"><a href="#" style="position: relative; z-index: 2; width: 28px; height: 28px; cursor: pointer; display: block; overflow: hidden; border-bottom: 0px none; box-sizing: content-box !important;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-in-small-normal.png" width="28" height="28" alt="지도 확대" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 28px; height: 28px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"></a><div style="position: relative; width: 28px; height: 216px; overflow: hidden; margin: 0px; padding: 7px 0px; background-color: rgb(255, 255, 255); cursor: pointer; box-sizing: content-box !important; display: none;"><div style="position: absolute; top: 7px; bottom: 7px; left: 12px; width: 4px; height: 216px; display: block; background-color: rgb(47, 135, 236);"></div><div style="position: absolute; top: 7px; bottom: 7px; left: 12px; width: 4px; height: 44px; display: block; background-color: rgb(202, 205, 209);"></div><a href="#" style="position: absolute; left: 4px; width: 18px; height: 10px; top: 44px; border: 1px solid rgb(68, 68, 68); cursor: move; display: block; overflow: hidden; box-sizing: content-box !important;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-handle.png" width="18" height="10" alt="지도 확대/축소 슬라이더" style="margin:0;padding:0;border:solid 0 transparent;display:block;box-sizing:content-box !important;max-width:none !important;max-height:none !important;min-width:0 !important;min-height:0 !important;width:18px;height:10px;"></a></div><a href="#" style="position: relative; z-index: 2; width: 28px; height: 28px; cursor: pointer; display: block; overflow: hidden; border-top: 1px solid rgb(202, 205, 209); box-sizing: content-box !important;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-out-small-normal.png" width="28" height="28" alt="지도 축소" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 28px; height: 28px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"></a><div style="position: absolute; top: 22px; width: 44px; height: 0px; overflow: visible; display: none; left: -51px;"><div style="display: block; margin: 0px; padding: 0px;"><h4 style="visibility:hidden;width:0;height:0;overflow:hidden;margin:0;padding:0;">지도 컨트롤러 범례</h4><div style="position: absolute; top: 43px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-on.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">부동산</span></div><div style="position: absolute; top: 63px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-normal.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">거리</span></div><div style="position: absolute; top: 83px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-normal.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">읍,면,동</span></div><div style="position: absolute; top: 113px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-normal.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">시,군,구</span></div><div style="position: absolute; top: 143px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-normal.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">시,도</span></div><div style="position: absolute; top: 163px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-normal.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">국가</span></div></div></div></div></div></div></div></div>
                                        <img src="https://simg.pstatic.net/static.map/v2/map/staticmap.bin?caller=smarteditor&amp;markers=pos%3A129.1106882%2035.1449906%7CviewSizeRatio%3A0.7%7Ctype%3Ad%7Ccolor%3A0x11cc73%7Csize%3Amid&amp;w=700&amp;h=315&amp;scale=2&amp;dataversion=174.22" alt="" class="se-map-image egjs-visible" style="display: none;">
                                    </div>
                                        <div class="se-module se-module-map-text ">
                                                <a href="#" target="_blank" class="se-map-info __se_link" onclick="return false;" data-linktype="map" data-linkdata="{&quot;eventTarget&quot; : &quot;placeDesc&quot;, &quot;placeId&quot; : &quot;1194149183&quot;, &quot;searchEngine&quot; : &quot;naver&quot;, &quot;searchType&quot; : &quot;s&quot;, &quot;name&quot; : &quot;안목&quot;, &quot;address&quot; : &quot;부산광역시 수영구 광남로22번길 3 1층 101호&quot;, &quot;latitude&quot; : &quot;35.1449906&quot;, &quot;longitude&quot; : &quot;129.1106882&quot;, &quot;tel&quot; : &quot;0507-1461-0523&quot;, &quot;bookingUrl&quot; : null }">
                                                <strong class="se-map-title">안목</strong>
                                                <p class="se-map-address">부산광역시 수영구 광남로22번길 3 1층 101호</p>
                                            </a>
                                        </div>
                                
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module="{&quot;type&quot;:&quot;v2_map&quot;, &quot;id&quot; :&quot;SE-c94683a8-9f85-495a-b23b-88cb68e1e261&quot;, &quot;data&quot; : { &quot;layout&quot;: &quot;default&quot;, &quot;searchEngine&quot; : &quot;naver&quot;, &quot;places&quot; : [{&quot;placeId&quot;:&quot;1194149183&quot;,&quot;name&quot;:&quot;안목&quot;,&quot;address&quot;:&quot;부산광역시 수영구 광남로22번길 3 1층 101호&quot;,&quot;latlng&quot;:{&quot;@ctype&quot;:&quot;position&quot;,&quot;latitude&quot;:35.1449906,&quot;longitude&quot;:129.1106882},&quot;searchType&quot;:&quot;s&quot;,&quot;tel&quot;:&quot;0507-1461-0523&quot;,&quot;bookingUrl&quot;:null}] }}" data-module-v2="{&quot;type&quot;:&quot;v2_map&quot;, &quot;id&quot; :&quot;SE-c94683a8-9f85-495a-b23b-88cb68e1e261&quot;, &quot;data&quot; : { &quot;layout&quot;: &quot;default&quot;, &quot;searchEngine&quot; : &quot;naver&quot;, &quot;places&quot; : [{&quot;placeId&quot;:&quot;1194149183&quot;,&quot;name&quot;:&quot;안목&quot;,&quot;address&quot;:&quot;부산광역시 수영구 광남로22번길 3 1층 101호&quot;,&quot;latlng&quot;:{&quot;@ctype&quot;:&quot;position&quot;,&quot;latitude&quot;:35.1449906,&quot;longitude&quot;:129.1106882},&quot;searchType&quot;:&quot;s&quot;,&quot;tel&quot;:&quot;0507-1461-0523&quot;,&quot;bookingUrl&quot;:null}] }}"></script>
                        </div>                <div class="se-component se-text se-l-default" id="SE-4cc48a44-4666-4e23-8292-7b28a3fa3b81">
                            <div class="se-component-content">
                                <div class="se-section se-section-text se-l-default">
                                    <div class="se-module se-module-text">
                                            <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-eaa8b6f4-97ab-4fb3-be61-7066d8dea12d"><span style="" class="se-fs-fs16 se-ff-   " id="SE-48aa3881-c6a3-4787-9457-fd7a649299e1">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-c37c996f-d9c0-4eae-bc30-759e3810220f"><span style="" class="se-fs-fs16 se-ff-   " id="SE-f501a030-3e72-4c20-96aa-d490e05c0798">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-a0ed9763-6598-4fcd-aea3-2811a92eb9aa"><span style="" class="se-fs-fs16 se-ff-   " id="SE-03db0124-e1ea-425f-8d23-ec0c024f1969">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-74fe50a3-9971-4bf6-8aed-3e6b65c48dc6"><span style="" class="se-fs-fs16 se-ff-   " id="SE-9b56fdc9-561e-492e-8ad2-351c79576e91">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                                    </div>
                                </div>
                            </div>
                            <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-4cc48a44-4666-4e23-8292-7b28a3fa3b81&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                        </div>    <div class="ssp-adcontent align_center"><div id="ssp-adcontent" class="ssp_adcontent_inner"><div style="width: 100%; height: auto; margin: 0px auto; line-height: 0;"><iframe id="ssp-adcontent_tgtLREC" frameborder="no" scrolling="no" tabindex="0" name="" title="AD" style="width: 100%; height: 211px; visibility: inherit; border: 0px; vertical-align: bottom;"></iframe></div></div></div></div>""",
                "title": "안목",
                "summary": "국밥 맛집 홍보"
            },
            {
                "raw_html": """<div class="se-main-container">
                <div class="se-component se-sticker se-l-default" id="SE-0738661f-4a49-11f0-9028-576461e712f2">
                    <div class="se-component-content">
                        <div class="se-section se-section-sticker se-section-align-right se-l-default">
                            <div class="se-module se-module-sticker">
                                <a href="#" onclick="return false;" class="__se_sticker_link __se_link" data-linktype="sticker" data-linkdata="{&quot;src&quot; : &quot;&quot;, &quot;packCode&quot; : &quot;ogq_631b8ca2652bc&quot;, &quot;seq&quot; : &quot;9&quot;, &quot;width&quot; : &quot;&quot;, &quot;height&quot; : &quot;&quot;}">
                                    <img src="https://storep-phinf.pstatic.net/ogq_631b8ca2652bc/original_9.png?type=p100_100" alt="" class="se-sticker-image egjs-visible">
                                </a>
                            </div>
                        </div>
                    </div>
                </div>                <div class="se-component se-quotation se-l-default" id="SE-6b002e3e-be15-45a1-8d3f-7efa1899c52d">
                    <div class="se-component-content">
                        <div class="se-section se-section-quotation se-l-default">
                            <blockquote class="se-quotation-container">
                                <div class="se-module se-module-text se-quote"><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-d6c9261d-7bd0-47c2-8e03-a4b1090ee3e9"><span style="" class="se-fs-fs15 se-ff-  se-style-unset " id="SE-094d8a83-4a49-11f0-9028-27b06e43a86e"><b>서울 미쉐린맛집 한식전문 목멱산방</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-9fcbb86f-8f25-4746-bd8d-bf50e678858a"><span style="" class="se-fs-fs13 se-ff-  se-style-unset " id="SE-094d8a84-4a49-11f0-9028-3de1dd97c11d"><b>-투쁠한우 육회비빔밥</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-e94c5abd-d405-4e9d-afb9-8f0240834c3a"><span style="" class="se-fs-fs13 se-ff-  se-style-unset " id="SE-094d8a85-4a49-11f0-9028-5f66380e008d"><b>-검은깨두부 보쌈</b></span></p><!-- } SE-TEXT --></div>
                            </blockquote>
                        </div>
                    </div>
                </div>
                <div class="se-component se-image se-l-default __se-component" id="SE-11a66dae-042e-4d6e-8f6b-35df63be4b88">
                    <div class="se-component-content se-component-content-fit">
                        <div class="se-section se-section-image se-l-default se-section-align-center">
                                <div class="se-module se-module-image" style="">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-11a66dae-042e-4d6e-8f6b-35df63be4b88&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfMzAw/MDAxNzUwMDA0NjUzODc3.-B773zgtfT-qiFwGYT2v9Ly8Ml1DJaJqeIJ4q09zxrYg.qZL-yBVM0PwdAqmMBF4MNf2XQ_vUTRNnDQAVQS5q4mEg.JPEG/1.JPG&quot;, &quot;originalWidth&quot; : &quot;4032&quot;, &quot;originalHeight&quot; : &quot;3024&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfMzAw/MDAxNzUwMDA0NjUzODc3.-B773zgtfT-qiFwGYT2v9Ly8Ml1DJaJqeIJ4q09zxrYg.qZL-yBVM0PwdAqmMBF4MNf2XQ_vUTRNnDQAVQS5q4mEg.JPEG/1.JPG?type=w773" data-lazy-src="" data-width="693" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-11a66dae-042e-4d6e-8f6b-35df63be4b88_0">
                                    </a>
                                </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-11a66dae-042e-4d6e-8f6b-35df63be4b88&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot; }}"></script>
                </div>
                <div class="se-component se-quotation se-l-quotation_postit" id="SE-ddaaa4e3-9fbb-49ea-8741-5e7b9af62162">
                    <div class="se-component-content">
                        <div class="se-section se-section-quotation se-l-quotation_postit">
                            <blockquote class="se-quotation-container">
                                <div class="se-module se-module-text se-quote"><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-73fe0b86-3851-4c42-9839-d129bbe609bf"><span style="" class="se-fs-fs11 se-ff-   " id="SE-094d8a86-4a49-11f0-9028-4f53c30fb52c"><b>서울 중구 퇴계로20길 71</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-47abb01a-f8af-4892-886c-38f1b57a79f2"><span style="" class="se-fs-fs11 se-ff-   " id="SE-094d8a87-4a49-11f0-9028-efd1028e16fe"><b>&ZeroWidthSpace;</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-e656281e-a19c-41c6-a9d0-f36e2eb942c9"><span style="" class="se-fs-fs11 se-ff-   " id="SE-094d8a88-4a49-11f0-9028-4dd588be36c2"><b>영업시간</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-72ca0270-1998-4e8d-98a8-de65a480767f"><span style="" class="se-fs-fs11 se-ff-   " id="SE-094d8a89-4a49-11f0-9028-bbdb982fca9e"><b>매일</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-d65bb3a2-88d4-49ec-abfc-d2f24fce5792"><span style="" class="se-fs-fs11 se-ff-   " id="SE-094d8a8a-4a49-11f0-9028-1379d0d3ec50"><b>11:00 - 20:00</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-d1f6a846-7367-42d6-8a58-a8241b904619"><span style="" class="se-fs-fs11 se-ff-   " id="SE-094d8a8b-4a49-11f0-9028-5df9420ad447"><b>라스트오더</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-9d2d6fc7-3c15-4343-9e62-76a73fa8b8c1"><span style="" class="se-fs-fs11 se-ff-   " id="SE-094d8a8c-4a49-11f0-9028-1bbc127810e9"><b>19:20</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-25842693-041c-40cc-a400-acaa3cdff810"><span style="" class="se-fs-fs11 se-ff-   " id="SE-094d8a8d-4a49-11f0-9028-730a9abdcc6a"><b>&ZeroWidthSpace;</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-54bc66bd-083a-47ae-b6f1-28ba05bb3f6e"><span style="" class="se-fs-fs11 se-ff-   " id="SE-094d8a8e-4a49-11f0-9028-794fa4eaa4ac"><b>전화</b></span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-470777c5-f9d7-4ca4-8893-5cc1ad0fd4d9"><span style="" class="se-fs-fs11 se-ff-   " id="SE-094db19f-4a49-11f0-9028-a9ef24060636"><b>02-318-4790</b></span></p><!-- } SE-TEXT --></div>
                            </blockquote>
                        </div>
                    </div>
                </div>
                <div class="se-component se-text se-l-default" id="SE-dc76941a-6798-4cbb-8800-8c9847ff0ec5">
                    <div class="se-component-content">
                        <div class="se-section se-section-text se-l-default">
                            <div class="se-module se-module-text">
                                    <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-c71a4369-17e6-4a7b-957c-f36bfa6e71d4"><span style="" class="se-fs- se-ff-   " id="SE-094db1a0-4a49-11f0-9028-1540e81fbeb1">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-dc76941a-6798-4cbb-8800-8c9847ff0ec5&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                </div>                <div class="se-component se-image se-l-default __se-component" id="SE-032794ac-8ded-4148-a0ea-be444e6673cb">
                    <div class="se-component-content se-component-content-fit">
                        <div class="se-section se-section-image se-l-default se-section-align-center">
                                <div class="se-module se-module-image" style="">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-032794ac-8ded-4148-a0ea-be444e6673cb&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfMjI0/MDAxNzUwMDA0NjUzNjEx.pUENI58wLVHgf07W6F6BNv4H02lqKWZ-o6Dr_TOQjakg.K58jd-T22Hjl3Pdxun_Km1pC68bhnmuY3hbs5y7S3Pcg.JPEG/2.JPG&quot;, &quot;originalWidth&quot; : &quot;4032&quot;, &quot;originalHeight&quot; : &quot;3024&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfMjI0/MDAxNzUwMDA0NjUzNjEx.pUENI58wLVHgf07W6F6BNv4H02lqKWZ-o6Dr_TOQjakg.K58jd-T22Hjl3Pdxun_Km1pC68bhnmuY3hbs5y7S3Pcg.JPEG/2.JPG?type=w773" data-lazy-src="" data-width="693" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-032794ac-8ded-4148-a0ea-be444e6673cb_0">
                                    </a>
                                </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-032794ac-8ded-4148-a0ea-be444e6673cb&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot; }}"></script>
                </div>
                <div class="se-component se-text se-l-default" id="SE-97208684-ac54-4d59-ada8-0be23caa1804">
                    <div class="se-component-content">
                        <div class="se-section se-section-text se-l-default">
                            <div class="se-module se-module-text">
                                    <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-81923234-4753-497b-8bab-38c1c859f0c9"><span style="" class="se-fs- se-ff-   " id="SE-094db1a1-4a49-11f0-9028-0b274433f553">서울 남산은 참 묘한 매력이 있는 곳 같아요!</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-34f3ab43-737f-444a-9e45-c4c36a2b41b7"><span style="" class="se-fs- se-ff-   " id="SE-094db1a2-4a49-11f0-9028-8304247b99ca">도시 속인데도 한 발짝만 올라오면 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-9b5d0cf1-342b-4a6c-aff4-8975a52e0119"><span style="" class="se-fs- se-ff-   " id="SE-094db1a3-4a49-11f0-9028-956c1a99f440">바람도 다르고, 공기도 다르고, </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-d3c35e3f-889c-440d-b8cf-fcf32497a7bf"><span style="" class="se-fs- se-ff-   " id="SE-094db1a4-4a49-11f0-9028-85fd64044da7">마음까지 탁 트이는 그런 느낌!</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-892e6f57-efc4-48fe-b143-ed5ccea42f9a"><span style="" class="se-fs- se-ff-   " id="SE-094db1a5-4a49-11f0-9028-511afec84483">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-ab1c1e4e-49ad-4619-b80f-e2a43dd8c048"><span style="" class="se-fs- se-ff-   " id="SE-094db1a6-4a49-11f0-9028-cbe1246f12b7">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-97208684-ac54-4d59-ada8-0be23caa1804&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                </div>                <div class="se-component se-image se-l-default __se-component" id="SE-d41829be-7570-46bc-9a53-efb98887dbbb">
                    <div class="se-component-content se-component-content-fit">
                        <div class="se-section se-section-image se-l-default se-section-align-center">
                                <div class="se-module se-module-image" style="">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-d41829be-7570-46bc-9a53-efb98887dbbb&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfMjE3/MDAxNzUwMDA0NjUzNjAy.7XwF2naP_fZhSbquAp47GU0NVmO1pazLZ5-upAEfodsg.4r2gA0a0ON61QSnYIIP_YmyRnM2zlCmrCkJl9esORWMg.JPEG/3.JPG&quot;, &quot;originalWidth&quot; : &quot;4032&quot;, &quot;originalHeight&quot; : &quot;3024&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfMjE3/MDAxNzUwMDA0NjUzNjAy.7XwF2naP_fZhSbquAp47GU0NVmO1pazLZ5-upAEfodsg.4r2gA0a0ON61QSnYIIP_YmyRnM2zlCmrCkJl9esORWMg.JPEG/3.JPG?type=w773" data-lazy-src="" data-width="693" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-d41829be-7570-46bc-9a53-efb98887dbbb_0">
                                    </a>
                                </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-d41829be-7570-46bc-9a53-efb98887dbbb&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot; }}"></script>
                </div>
                <div class="se-component se-text se-l-default" id="SE-99e80f51-a74e-4406-972c-10e5d217751c">
                    <div class="se-component-content">
                        <div class="se-section se-section-text se-l-default">
                            <div class="se-module se-module-text">
                                    <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-1b5d1365-1e7e-44ba-805a-1f85848329b0"><span style="" class="se-fs- se-ff-   " id="SE-094db1a7-4a49-11f0-9028-df6f7500ce7c">그런 남산 한켠에 있는 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-d51a8159-dae5-433f-b66f-a574e89dcf68"><span style="" class="se-fs- se-ff-   " id="SE-094db1a8-4a49-11f0-9028-175f2cce2af1">서울 미쉐린 맛집</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-70c3c136-83f2-4319-93e7-b98d97f547c5"><span style="" class="se-fs- se-ff-   " id="SE-094db1a9-4a49-11f0-9028-512747ee30da">목멱산방 본점에서 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-12d67aff-fb2d-4d40-bc4f-17c04df47554"><span style="" class="se-fs- se-ff-   " id="SE-094db1aa-4a49-11f0-9028-afd2d4ccb811">특별한 한 끼를 즐기고 왔어요!</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-bc902279-0d32-4e6b-8d98-753149e61884"><span style="" class="se-fs- se-ff-   " id="SE-094db1ab-4a49-11f0-9028-938a1ab19800">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-fd0fffe9-a7ec-417b-a851-fc48f366343b"><span style="" class="se-fs- se-ff-   " id="SE-094dd8bc-4a49-11f0-9028-1d9474b8b993">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-99e80f51-a74e-4406-972c-10e5d217751c&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                </div>                <div class="se-component se-image se-l-default __se-component" id="SE-1b7deae3-47ec-4392-b170-a43640ec3cc2">
                    <div class="se-component-content se-component-content-fit">
                        <div class="se-section se-section-image se-l-default se-section-align-center">
                                <div class="se-module se-module-image" style="">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-1b7deae3-47ec-4392-b170-a43640ec3cc2&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfMTYy/MDAxNzUwMDA0NjUzOTQ1.-t8HWvzFIA9SZNva1uR6nkGJlQAtlAe9jnPNed5sBbMg.OpA-wn3ZUvc1chxNXLR8NbMfs0F1KknwPfYnXFzVKDAg.JPEG/4.JPG&quot;, &quot;originalWidth&quot; : &quot;4032&quot;, &quot;originalHeight&quot; : &quot;3024&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfMTYy/MDAxNzUwMDA0NjUzOTQ1.-t8HWvzFIA9SZNva1uR6nkGJlQAtlAe9jnPNed5sBbMg.OpA-wn3ZUvc1chxNXLR8NbMfs0F1KknwPfYnXFzVKDAg.JPEG/4.JPG?type=w773" data-lazy-src="" data-width="693" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-1b7deae3-47ec-4392-b170-a43640ec3cc2_0">
                                    </a>
                                </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-1b7deae3-47ec-4392-b170-a43640ec3cc2&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot; }}"></script>
                </div>
                <div class="se-component se-text se-l-default" id="SE-d2eec614-64d0-43fc-a160-a3cf8e96c603">
                    <div class="se-component-content">
                        <div class="se-section se-section-text se-l-default">
                            <div class="se-module se-module-text">
                                    <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-9f7e27e0-7e58-402e-af3d-48789eec0282"><span style="" class="se-fs- se-ff-   " id="SE-094dd8bd-4a49-11f0-9028-5f886cde3903">식사 중간중간 보니 외국인 관광객도 많았고</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-8edbee5b-9824-4d10-9598-e733afc031c1"><span style="" class="se-fs- se-ff-   " id="SE-094dd8be-4a49-11f0-9028-43c80ca61549">데이트나 가족 외식으로 많이들 오더라고요~</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-67e592f2-9442-4634-b335-8e5e8676b0dd"><span style="" class="se-fs- se-ff-   " id="SE-094dd8bf-4a49-11f0-9028-b9ee41d9bc6b">실내는 군더더기 없이 깔끔하고 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-e4be414d-8cd4-4af9-9563-ba60d5d335df"><span style="" class="se-fs- se-ff-   " id="SE-094dd8c0-4a49-11f0-9028-d3544d5365c5">모던한 느낌이라 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-1ffcb619-314b-48c7-9b2c-cb1cd4d8fa65"><span style="" class="se-fs- se-ff-   " id="SE-094dd8c1-4a49-11f0-9028-790d22174ca2">전통 한식을 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-a50d8595-77bf-4ef1-afd4-a755d8d0993f"><span style="" class="se-fs- se-ff-   " id="SE-094dd8c2-4a49-11f0-9028-518343b85eb8">더 세련되게 느낄 수 있어요.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-f29db176-0aae-4a2b-a5ed-78c7e3587942"><span style="" class="se-fs- se-ff-   " id="SE-094dd8c3-4a49-11f0-9028-856c98d4f86f">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-87e878a7-c783-4a2c-9462-d1c2b2e77bb1"><span style="" class="se-fs- se-ff-   " id="SE-094dd8c4-4a49-11f0-9028-43610a239917">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-d2eec614-64d0-43fc-a160-a3cf8e96c603&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                </div>                <div class="ssp-adcontent align_center"><div id="ssp-adcontent-1" class="ssp_adcontent_inner"><div style="width: 100%; height: auto; margin: 0px auto; line-height: 0;"><iframe id="ssp-adcontent-1_tgtLREC" frameborder="no" scrolling="no" tabindex="0" name="" title="AD" style="width: 100%; height: 170px; visibility: inherit; border: 0px; vertical-align: bottom;"></iframe></div></div></div><div class="se-component se-image se-l-default __se-component" id="SE-3bcfcc34-922e-4bb1-a56a-43af4a429aeb">
                    <div class="se-component-content se-component-content-fit">
                        <div class="se-section se-section-image se-l-default se-section-align-center">
                                <div class="se-module se-module-image" style="">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-3bcfcc34-922e-4bb1-a56a-43af4a429aeb&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfMjQ3/MDAxNzUwMDA0NjUzOTE2.2bv-UBNqQdEUREfWjLpYBgr1ieH_k7M1GQ-cyREhWWUg.tygu7WSjy20OuFinUdb8XTZbqgGq0vuyStMTMJ8iSnEg.JPEG/5.JPG&quot;, &quot;originalWidth&quot; : &quot;3024&quot;, &quot;originalHeight&quot; : &quot;4032&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfMjQ3/MDAxNzUwMDA0NjUzOTE2.2bv-UBNqQdEUREfWjLpYBgr1ieH_k7M1GQ-cyREhWWUg.tygu7WSjy20OuFinUdb8XTZbqgGq0vuyStMTMJ8iSnEg.JPEG/5.JPG?type=w773" data-lazy-src="" data-width="693" data-height="924" alt="" class="se-image-resource egjs-visible" id="SE-3bcfcc34-922e-4bb1-a56a-43af4a429aeb_0">
                                    </a>
                                </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-3bcfcc34-922e-4bb1-a56a-43af4a429aeb&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot; }}"></script>
                </div>
                <div class="se-component se-text se-l-default" id="SE-fd14f80c-9b79-4ecf-80a8-e2ab3d344457">
                    <div class="se-component-content">
                        <div class="se-section se-section-text se-l-default">
                            <div class="se-module se-module-text">
                                    <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-704a902b-a5c9-4d93-88b6-80e8987db6b8"><span style="" class="se-fs- se-ff-   " id="SE-094dd8c5-4a49-11f0-9028-fb40f85d2e97">주문은 셀프 방식으로 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-70f42a7b-7df2-4d99-bce6-5083071add22"><span style="" class="se-fs- se-ff-   " id="SE-094dd8c6-4a49-11f0-9028-a3c1f9c39528">키오스크로 하면돼요~</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-92dfa0d0-c128-4fd4-ac43-cf2118df8fbe"><span style="" class="se-fs- se-ff-   " id="SE-094dd8c7-4a49-11f0-9028-37329d8c97cc">방송에도 여러번 나오고 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-3073c8cb-cde1-4bb5-87da-7afef3566598"><span style="" class="se-fs- se-ff-   " id="SE-094dd8c8-4a49-11f0-9028-7d8a235424a3">미쉐린 맛집답게</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-0a353210-f8b2-4ee3-bcc9-f6641f0567d9"><span style="" class="se-fs- se-ff-   " id="SE-094dd8c9-4a49-11f0-9028-0388adb015d0">주말에는 사람이 많아요!</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-dc70a503-d34c-4cc9-af39-06c174d9c4ac"><span style="" class="se-fs- se-ff-   " id="SE-094dd8ca-4a49-11f0-9028-7dacaa80bcb2">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-77cc88c2-a044-48f9-94b0-6d9d30871172"><span style="" class="se-fs- se-ff-   " id="SE-094dd8cb-4a49-11f0-9028-7d2c85e24e79">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-fd14f80c-9b79-4ecf-80a8-e2ab3d344457&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                </div>                <div class="se-component se-horizontalLine se-l-line3" id="SE-ba6ff12f-4399-410c-9d94-2afcf7c8088e">
                    <div class="se-component-content">
                        <div class="se-section se-section-horizontalLine se-l-line3 se-section-align-center">
                            <div class="se-module se-module-horizontalLine">
                                <hr class="se-hr">
                            </div>
                        </div>
                    </div>
                </div>                <div class="se-component se-image se-l-default __se-component" id="SE-add22dd7-4a10-11f0-b739-7f2d8d792dbc">
                    <div class="se-component-content se-component-content-normal">
                        <div class="se-section se-section-image se-l-default se-section-align-center" style="max-width:519px;">
                                <div class="se-module se-module-image" style="">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-add22dd7-4a10-11f0-b739-7f2d8d792dbc&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfMTMx/MDAxNzUwMDA5NTk2MTI4.zH-8q2PF4NpuBiUVX5RJjpK5fc6IZHAQsUENLnsuK3Mg.ILZhTqdZEvGedH80YTDH4LFZs4DPIsqfjDMEQLVNvZYg.JPEG/900%EF%BC%BF20250616%EF%BC%BF024555.jpg&quot;, &quot;originalWidth&quot; : &quot;900&quot;, &quot;originalHeight&quot; : &quot;900&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfMTMx/MDAxNzUwMDA5NTk2MTI4.zH-8q2PF4NpuBiUVX5RJjpK5fc6IZHAQsUENLnsuK3Mg.ILZhTqdZEvGedH80YTDH4LFZs4DPIsqfjDMEQLVNvZYg.JPEG/900%EF%BC%BF20250616%EF%BC%BF024555.jpg?type=w773" data-lazy-src="" data-width="519" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-add22dd7-4a10-11f0-b739-7f2d8d792dbc_0">
                                    </a>
                                </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-add22dd7-4a10-11f0-b739-7f2d8d792dbc&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot; }}"></script>
                </div>
                <div class="se-component se-text se-l-default" id="SE-7b9eeb92-8159-4c6c-ad8e-6839d2d295a2">
                    <div class="se-component-content">
                        <div class="se-section se-section-text se-l-default">
                            <div class="se-module se-module-text">
                                    <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-5c2fb550-50b2-414c-82a3-d9be744fe06f"><span style="" class="se-fs- se-ff-   " id="SE-094dffdc-4a49-11f0-9028-01463d113f2b">이날 저희가 선택한 메뉴는 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-0e7bdd4a-505a-4a8a-916c-90b1bdc61b28"><span style="" class="se-fs- se-ff-   " id="SE-094dffdd-4a49-11f0-9028-6342041393c5">검은깨두부와 보쌈, </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-6dd16410-f309-4282-883f-07ca866188f0"><span style="" class="se-fs- se-ff-   " id="SE-094dffde-4a49-11f0-9028-2d51b0e14efa">그리고 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-734c7eb0-33c4-4fae-b04d-68ce4ef672c8"><span style="" class="se-fs- se-ff-   " id="SE-094dffdf-4a49-11f0-9028-758950043218">시그니처 메뉴인 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-399ee4d1-7a01-40f9-bc44-c9859d5165e3"><span style="" class="se-fs- se-ff-   " id="SE-094dffe0-4a49-11f0-9028-83c89e85bbcd">투뿔한우 육회비빔밥을 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-4eefc4e3-4978-48fa-b1b7-b028928dfae6"><span style="" class="se-fs- se-ff-   " id="SE-094dffe1-4a49-11f0-9028-413d71aedec4">주문했는데</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-7dd99cb5-4d03-4f04-bfd8-8a9dc6ebcc2e"><span style="" class="se-fs- se-ff-   " id="SE-094dffe2-4a49-11f0-9028-2beae681ce58">기대 이상이었어요!</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-2761b65a-5f55-4e32-874e-4fb3c74f73c9"><span style="" class="se-fs- se-ff-   " id="SE-094dffe3-4a49-11f0-9028-553184ed4f75">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-835bf759-eebb-41d3-8771-96a35d16285f"><span style="" class="se-fs- se-ff-   " id="SE-094dffe4-4a49-11f0-9028-03d7944878e1">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-7b9eeb92-8159-4c6c-ad8e-6839d2d295a2&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                </div>                <div class="se-component se-quotation se-l-quotation_bubble" id="SE-919b374c-3441-42c9-a0a1-190fabe16a59">
                    <div class="se-component-content">
                        <div class="se-section se-section-quotation se-l-quotation_bubble">
                            <blockquote class="se-quotation-container">
                                <div class="se-module se-module-text se-quote"><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-fe39d043-950a-41a5-a51e-40094299ff31"><span style="" class="se-fs- se-ff-   " id="SE-094dffe5-4a49-11f0-9028-77afa8ce6e86">검은깨두부&amp;보쌈</span></p><!-- } SE-TEXT --></div>
                            </blockquote>
                        </div>
                    </div>
                </div>
                <div class="se-component se-image se-l-default __se-component" id="SE-fc552731-ffd3-49e3-9a87-3c1c5d5c2f4f">
                    <div class="se-component-content se-component-content-fit">
                        <div class="se-section se-section-image se-l-default se-section-align-center">
                                <div class="se-module se-module-image" style="">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-fc552731-ffd3-49e3-9a87-3c1c5d5c2f4f&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfMjUz/MDAxNzUwMDA0NjUzNzA5.oaN1fVRAiffc4Iv38YUe1uxZIMGHUFc3UBwwebGuvHYg.YzL4gD9cC0WthYAyF63wLR7fqItiQHn58sJNEurOYiUg.JPEG/6.JPG&quot;, &quot;originalWidth&quot; : &quot;4032&quot;, &quot;originalHeight&quot; : &quot;3024&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfMjUz/MDAxNzUwMDA0NjUzNzA5.oaN1fVRAiffc4Iv38YUe1uxZIMGHUFc3UBwwebGuvHYg.YzL4gD9cC0WthYAyF63wLR7fqItiQHn58sJNEurOYiUg.JPEG/6.JPG?type=w773" data-lazy-src="" data-width="693" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-fc552731-ffd3-49e3-9a87-3c1c5d5c2f4f_0">
                                    </a>
                                </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-fc552731-ffd3-49e3-9a87-3c1c5d5c2f4f&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot; }}"></script>
                </div>
                <div class="se-component se-text se-l-default" id="SE-1d8cf307-2baf-4e89-ac83-d7ad4d0430fe">
                    <div class="se-component-content">
                        <div class="se-section se-section-text se-l-default">
                            <div class="se-module se-module-text">
                                    <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-cb802b9c-edec-45d5-9406-259645d590e8"><span style="" class="se-fs- se-ff-   " id="SE-094dffe6-4a49-11f0-9028-a1d0167b6f85">먼저 검은깨두부와 보쌈!!</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-a209f5d6-5081-412c-97ae-ef35cac5a3e9"><span style="" class="se-fs- se-ff-   " id="SE-094dffe7-4a49-11f0-9028-0391f727bbd0">검은깨 두부는</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-867430c4-538d-4914-8c77-1b24059221ef"><span style="" class="se-fs- se-ff-   " id="SE-094dffe8-4a49-11f0-9028-2125f0ac11f6">보기만 해도 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-cf1b94c3-9dab-415e-ad68-05e05b30a1d2"><span style="" class="se-fs- se-ff-   " id="SE-094dffe9-4a49-11f0-9028-f34891ccdcc5">고소한 향이 물씬 풍기는것같고</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-9f92d8f8-9db0-4061-ad4c-bd1468319cad"><span style="" class="se-fs- se-ff-   " id="SE-094dffea-4a49-11f0-9028-4310ccdc6f4d">입에 넣자마자 사르르 녹아요!!</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-446038b6-7eb1-4338-b445-ba804d2e6ff3"><span style="" class="se-fs- se-ff-   " id="SE-094dffeb-4a49-11f0-9028-cd9c76368bd9">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-1d8cf307-2baf-4e89-ac83-d7ad4d0430fe&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                </div>                <div class="se-component se-image se-l-default __se-component" id="SE-ad678fae-f9db-4e0e-8698-7402ced6b1b1">
                    <div class="se-component-content se-component-content-fit">
                        <div class="se-section se-section-image se-l-default se-section-align-center">
                                <div class="se-module se-module-image" style="">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-ad678fae-f9db-4e0e-8698-7402ced6b1b1&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfMTMy/MDAxNzUwMDA0NjU1NDMw.jilgfE4Ws3ZriW90ViRyLFelKNc_r_D7W1ppJ-L5KZUg._WPRKxQhmjk7XIUtC3f0jtt08Px_STdlJJbCoGgzTk0g.JPEG/7.JPG&quot;, &quot;originalWidth&quot; : &quot;4032&quot;, &quot;originalHeight&quot; : &quot;3024&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfMTMy/MDAxNzUwMDA0NjU1NDMw.jilgfE4Ws3ZriW90ViRyLFelKNc_r_D7W1ppJ-L5KZUg._WPRKxQhmjk7XIUtC3f0jtt08Px_STdlJJbCoGgzTk0g.JPEG/7.JPG?type=w773" data-lazy-src="" data-width="693" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-ad678fae-f9db-4e0e-8698-7402ced6b1b1_0">
                                    </a>
                                </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-ad678fae-f9db-4e0e-8698-7402ced6b1b1&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot; }}"></script>
                </div>
                <div class="se-component se-text se-l-default" id="SE-a0891e02-19d5-409b-a4d3-5f527f1f41d7">
                    <div class="se-component-content">
                        <div class="se-section se-section-text se-l-default">
                            <div class="se-module se-module-text">
                                    <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-555321f3-27e4-48d7-a0c8-221593544d5b"><span style="" class="se-fs- se-ff-   " id="SE-094dffec-4a49-11f0-9028-b1b477dcefea">정말 진한 고소함이 입안에 퍼지는데, </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-a43a5af6-6eec-4d78-b633-a2bef1b7118d"><span style="" class="se-fs- se-ff-   " id="SE-094e26fd-4a49-11f0-9028-3b1591cba50d">이게 그냥 두부가 아니라는 걸 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-bcf71c1d-b733-4679-9b6d-4123533223ea"><span style="" class="se-fs- se-ff-   " id="SE-094e26fe-4a49-11f0-9028-0988ef0fae28">한입만 먹어도 느낄 수 있어요. </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-b0e47b75-961b-456c-863a-9c204ce9c900"><span style="" class="se-fs- se-ff-   " id="SE-094e26ff-4a49-11f0-9028-058416ded40a">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-a0891e02-19d5-409b-a4d3-5f527f1f41d7&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                </div>                <div class="se-component se-image se-l-default __se-component" id="SE-a82adb0e-df9c-4b38-a88b-b86689e01459">
                    <div class="se-component-content se-component-content-fit">
                        <div class="se-section se-section-image se-l-default se-section-align-center">
                                <div class="se-module se-module-image" style="">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-a82adb0e-df9c-4b38-a88b-b86689e01459&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfMjkg/MDAxNzUwMDA0NjU1NTEy.REZx3Q-TfYfsp3rXCMZZRFQOFuJBoKv67oLXEl4O00kg.EpddrJWGkqdaqwBEtBUpwsdc51UeoAWn4jd-cRxY5G0g.JPEG/8.JPG&quot;, &quot;originalWidth&quot; : &quot;4032&quot;, &quot;originalHeight&quot; : &quot;3024&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfMjkg/MDAxNzUwMDA0NjU1NTEy.REZx3Q-TfYfsp3rXCMZZRFQOFuJBoKv67oLXEl4O00kg.EpddrJWGkqdaqwBEtBUpwsdc51UeoAWn4jd-cRxY5G0g.JPEG/8.JPG?type=w773" data-lazy-src="" data-width="693" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-a82adb0e-df9c-4b38-a88b-b86689e01459_0">
                                    </a>
                                </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-a82adb0e-df9c-4b38-a88b-b86689e01459&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot; }}"></script>
                </div>
                <div class="se-component se-text se-l-default" id="SE-77871098-4118-4e9c-b1b6-d38154c6245d">
                    <div class="se-component-content">
                        <div class="se-section se-section-text se-l-default">
                            <div class="se-module se-module-text">
                                    <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-52ac2f2b-6959-42af-9e2b-552b94792a23"><span style="" class="se-fs- se-ff-   " id="SE-094e2700-4a49-11f0-9028-b1e016b9b804">그 두부와 함께 나오는 보쌈은 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-59d7f6d9-05aa-4a90-be08-b4b5ac52d9e2"><span style="" class="se-fs- se-ff-   " id="SE-094e2701-4a49-11f0-9028-bf05c604a1cd">지방과 살코기 비율이 완벽해서 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-35b7007e-2e0b-48c6-9e74-88739bc4d2ff"><span style="" class="se-fs- se-ff-   " id="SE-094e2702-4a49-11f0-9028-db4821b9ba39">쫀득하면서도 부드러워요.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-1eaf1850-bf7a-47b2-ab11-da7b20455f74"><span style="" class="se-fs- se-ff-   " id="SE-094e2703-4a49-11f0-9028-27265c97b29d">거기에 곁들여지는 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-1372fd4b-f733-4c9f-8a64-389592239a6f"><span style="" class="se-fs- se-ff-   " id="SE-094e2704-4a49-11f0-9028-bbbfbd918b5a">볶음김치와 특제 야채무침이 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-1486e42d-75a2-4b55-87e7-e0d824954244"><span style="" class="se-fs- se-ff-   " id="SE-094e2705-4a49-11f0-9028-eddda4939422">보쌈 맛을 확 살려줘서, </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-4722cb29-8e8e-4b7e-b53f-a4a87ded3c34"><span style="" class="se-fs- se-ff-   " id="SE-094e2706-4a49-11f0-9028-4157eea1306b">딱 한식의 진수라는 말이 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-34fb2235-11e3-4e9c-869f-fdb90b421f97"><span style="" class="se-fs- se-ff-   " id="SE-094e2707-4a49-11f0-9028-953b27478fcb">떠오르더라고요!</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-b163b937-6cd8-491e-b0d9-622bd3462089"><span style="" class="se-fs- se-ff-   " id="SE-094e2708-4a49-11f0-9028-1b6161e21557">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-547ff115-fb40-4e50-a784-9eee60ead05c"><span style="" class="se-fs- se-ff-   " id="SE-094e2709-4a49-11f0-9028-19b1d8261e0d">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-77871098-4118-4e9c-b1b6-d38154c6245d&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                </div>                <div class="se-component se-quotation se-l-quotation_bubble" id="SE-1b2a17b1-0a8d-4ba2-ac8f-da7087bf542f">
                    <div class="se-component-content">
                        <div class="se-section se-section-quotation se-l-quotation_bubble">
                            <blockquote class="se-quotation-container">
                                <div class="se-module se-module-text se-quote"><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-6d3ddcb0-40ea-414b-a56f-7e87f375792b"><span style="" class="se-fs- se-ff-   " id="SE-094e270a-4a49-11f0-9028-c57b50c13758">투쁠한우 육회비빔밥</span></p><!-- } SE-TEXT --></div>
                            </blockquote>
                        </div>
                    </div>
                </div>
                <div class="ssp-adcontent align_center"><div id="ssp-adcontent-2" class="ssp_adcontent_inner"><div style="width: 100%; height: auto; margin: 0px auto; line-height: 0;"><iframe id="ssp-adcontent-2_tgtLREC" frameborder="no" scrolling="no" tabindex="0" name="" title="AD" style="width: 100%; height: 170px; visibility: inherit; border: 0px; vertical-align: bottom;"></iframe></div></div></div><div class="se-component se-image se-l-default __se-component" id="SE-5bee08c3-c875-41b8-aa46-f3984f182984">
                    <div class="se-component-content se-component-content-fit">
                        <div class="se-section se-section-image se-l-default se-section-align-center">
                                <div class="se-module se-module-image" style="">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-5bee08c3-c875-41b8-aa46-f3984f182984&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfMjEw/MDAxNzUwMDA0NjU1NzEz.P6fmkmXI4uDi7KZ_8flDo3fga99U1zWEe-k9jpvnMzQg.wZ0Sy5q2g36XLIx1Ay9eGAN7plq7uqglsBo2yJ-tqW0g.JPEG/9.JPG&quot;, &quot;originalWidth&quot; : &quot;4032&quot;, &quot;originalHeight&quot; : &quot;3024&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfMjEw/MDAxNzUwMDA0NjU1NzEz.P6fmkmXI4uDi7KZ_8flDo3fga99U1zWEe-k9jpvnMzQg.wZ0Sy5q2g36XLIx1Ay9eGAN7plq7uqglsBo2yJ-tqW0g.JPEG/9.JPG?type=w773" data-lazy-src="" data-width="693" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-5bee08c3-c875-41b8-aa46-f3984f182984_0">
                                    </a>
                                </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-5bee08c3-c875-41b8-aa46-f3984f182984&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot; }}"></script>
                </div>
                <div class="se-component se-text se-l-default" id="SE-fe40dce8-e009-479e-a74d-726ee02ea25f">
                    <div class="se-component-content">
                        <div class="se-section se-section-text se-l-default">
                            <div class="se-module se-module-text">
                                    <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-cf8849bd-4e8b-4152-ad82-181b5343eaff"><span style="" class="se-fs- se-ff-   " id="SE-094e270b-4a49-11f0-9028-b13cbd68ab90">대망의 투쁠한우 육회비빔밥!</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-ebee9bb6-714b-4b4f-9d2f-9fabba23e401"><span style="" class="se-fs- se-ff-   " id="SE-094e270c-4a49-11f0-9028-9fe23359d7c7">비주얼도 예쁘고</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-dacb26b3-ed5e-49fd-83b1-06d91d66b352"><span style="" class="se-fs- se-ff-   " id="SE-094e270d-4a49-11f0-9028-0b58fd0c3b83">정말 먹음직 스러웠어요!</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-789784a8-cf2d-4285-a540-03b39c8b4ab0"><span style="" class="se-fs- se-ff-   " id="SE-094e270e-4a49-11f0-9028-7b1278c4cdcf">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-c292992d-0fa5-4c59-90b4-096a56ef2298"><span style="" class="se-fs- se-ff-   " id="SE-094e270f-4a49-11f0-9028-1d518d4f9499">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-fe40dce8-e009-479e-a74d-726ee02ea25f&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                </div>                <div class="se-component se-image se-l-default __se-component" id="SE-e2baa8fb-69a7-48fe-a429-3c312f7c93e8">
                    <div class="se-component-content se-component-content-fit">
                        <div class="se-section se-section-image se-l-default se-section-align-center">
                                <div class="se-module se-module-image" style="">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-e2baa8fb-69a7-48fe-a429-3c312f7c93e8&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfNjUg/MDAxNzUwMDA0NjU2MDYw.BOJ0WxM8BHXEUjMht2tT8JmLTn1lf8g6yDFugMG47-Qg.-FXwCZ0qlrTTeJSkA5V1EMa2b8gfXIJmnjEvca183bQg.JPEG/10.JPG&quot;, &quot;originalWidth&quot; : &quot;4032&quot;, &quot;originalHeight&quot; : &quot;3024&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfNjUg/MDAxNzUwMDA0NjU2MDYw.BOJ0WxM8BHXEUjMht2tT8JmLTn1lf8g6yDFugMG47-Qg.-FXwCZ0qlrTTeJSkA5V1EMa2b8gfXIJmnjEvca183bQg.JPEG/10.JPG?type=w773" data-lazy-src="" data-width="693" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-e2baa8fb-69a7-48fe-a429-3c312f7c93e8_0">
                                    </a>
                                </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-e2baa8fb-69a7-48fe-a429-3c312f7c93e8&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot; }}"></script>
                </div>
                <div class="se-component se-text se-l-default" id="SE-de39b829-513d-4750-a158-eb2cf44aeb6e">
                    <div class="se-component-content">
                        <div class="se-section se-section-text se-l-default">
                            <div class="se-module se-module-text">
                                    <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-8dd8912c-31fc-4577-93ab-fdc31599f795"><span style="" class="se-fs- se-ff-   " id="SE-094e4e20-4a49-11f0-9028-c321ffdb8b6a">이건 먼저 육회만 따로 맛봤는데, </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-403628f4-6254-4229-99ef-46e4da11afb9"><span style="" class="se-fs- se-ff-   " id="SE-094e4e21-4a49-11f0-9028-5171e65998ca">신선한 투뿔 채끝살에 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-8cd089c9-a3c2-4573-bc4b-53efb5447644"><span style="" class="se-fs- se-ff-   " id="SE-094e4e22-4a49-11f0-9028-8b37f40f3ad4">유자청과 꿀로 살짝 단맛을 더한 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-5938297d-8dd3-4f00-ace0-63cfa079976b"><span style="" class="se-fs- se-ff-   " id="SE-094e4e23-4a49-11f0-9028-3329adc3e153">양념이 어우러져, </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-f269246f-06df-48ba-8aa8-2bd14793b286"><span style="" class="se-fs- se-ff-   " id="SE-094e4e24-4a49-11f0-9028-89f347dc2849">하나도 느끼하지 않고 깔끔했어요.!!</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-5873b96d-2a52-45b9-9636-53d930338030"><span style="" class="se-fs- se-ff-   " id="SE-094e4e25-4a49-11f0-9028-5375597a0bcb">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-30641eb5-787e-46c4-a7dd-9b761250e0ba"><span style="" class="se-fs- se-ff-   " id="SE-094e4e26-4a49-11f0-9028-cb03ad4c3059">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-de39b829-513d-4750-a158-eb2cf44aeb6e&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                </div>                <div class="se-component se-image se-l-default __se-component" id="SE-f889823e-c2a3-4013-a77a-1382811af021">
                    <div class="se-component-content se-component-content-fit">
                        <div class="se-section se-section-image se-l-default se-section-align-center">
                                <div class="se-module se-module-image" style="">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-f889823e-c2a3-4013-a77a-1382811af021&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfMTc4/MDAxNzUwMDA0NjU2ODI5.B4vaInStzMCtfQwJNOd78vCE9Q-fiPB44SJXK89_GYEg.DznEmWgjfEa3kGhY7e7x4f69Rthce7gfWM0bPxADtIgg.JPEG/13.JPG&quot;, &quot;originalWidth&quot; : &quot;4032&quot;, &quot;originalHeight&quot; : &quot;3024&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfMTc4/MDAxNzUwMDA0NjU2ODI5.B4vaInStzMCtfQwJNOd78vCE9Q-fiPB44SJXK89_GYEg.DznEmWgjfEa3kGhY7e7x4f69Rthce7gfWM0bPxADtIgg.JPEG/13.JPG?type=w773" data-lazy-src="" data-width="693" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-f889823e-c2a3-4013-a77a-1382811af021_0">
                                    </a>
                                </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-f889823e-c2a3-4013-a77a-1382811af021&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot; }}"></script>
                </div>
                <div class="se-component se-text se-l-default" id="SE-8d381902-770a-44ad-943a-0e616932247f">
                    <div class="se-component-content">
                        <div class="se-section se-section-text se-l-default">
                            <div class="se-module se-module-text">
                                    <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-2ae2133e-6fe6-47ab-9a16-52c93ec41268"><span style="" class="se-fs- se-ff-   " id="SE-094e4e27-4a49-11f0-9028-1786e56781ed">비빔밥은 나물과 함께 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-a428d6ee-714d-4c06-a61b-8e7724f11bf5"><span style="" class="se-fs- se-ff-   " id="SE-094e4e28-4a49-11f0-9028-07f126849f86">조심스럽게 비벼 한입 먹었을 때,</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-34164201-98fa-4bcf-b056-1272cfbc5820"><span style="" class="se-fs- se-ff-   " id="SE-094e4e29-4a49-11f0-9028-d97cb57a5c79">고추장을 넣지 않고도 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-38bf2419-4d62-4a3a-95ad-8c65c0f3b530"><span style="" class="se-fs- se-ff-   " id="SE-094e4e2a-4a49-11f0-9028-8b4c5f6be3f8">양념된 육회와 참기름만으로 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-dadee1df-a5fb-48b9-ae7f-cd43d0983475"><span style="" class="se-fs- se-ff-   " id="SE-094e4e2b-4a49-11f0-9028-3b4b0a3a3058">깊은 맛이 나는 게, </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-04a66015-2067-4aec-812e-af4a540723d8"><span style="" class="se-fs- se-ff-   " id="SE-094e4e2c-4a49-11f0-9028-3d91c81587b4">정말 재료 하나하나에 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-834aa8bd-b8b9-4539-bf1e-c1dd1ad3af5a"><span style="" class="se-fs- se-ff-   " id="SE-094e4e2d-4a49-11f0-9028-911d84e2c8f7">얼마나 정성을 들였는지 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-bf27798c-c21a-4cb9-a092-71681aafc422"><span style="" class="se-fs- se-ff-   " id="SE-094e4e2e-4a49-11f0-9028-c11aa7fac120">알겠더라고요.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-8dc12133-87fd-42e0-a6b2-f9d72da31c53"><span style="" class="se-fs- se-ff-   " id="SE-094e4e2f-4a49-11f0-9028-9717122f27dc">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-cb26b645-1357-443b-aea8-02f97022939b"><span style="" class="se-fs- se-ff-   " id="SE-094e4e30-4a49-11f0-9028-87c4faffb9cf">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-8d381902-770a-44ad-943a-0e616932247f&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                </div>                <div class="se-component se-image se-l-default __se-component" id="SE-ae0dc305-e60a-498a-8ccb-8cbcfabec539">
                    <div class="se-component-content se-component-content-fit">
                        <div class="se-section se-section-image se-l-default se-section-align-center">
                                <div class="se-module se-module-image" style="">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-ae0dc305-e60a-498a-8ccb-8cbcfabec539&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfMTYx/MDAxNzUwMDA0NjU1NjMw.Z8CN5qEvNfDdPmjuwXwpF9hCV4CfWHWQ6eWip2obWpMg.9e1AyuTUWc3_coNrQOcarOUSZQo8HOioaImlMd9JJcAg.JPEG/11.JPG&quot;, &quot;originalWidth&quot; : &quot;4032&quot;, &quot;originalHeight&quot; : &quot;3024&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfMTYx/MDAxNzUwMDA0NjU1NjMw.Z8CN5qEvNfDdPmjuwXwpF9hCV4CfWHWQ6eWip2obWpMg.9e1AyuTUWc3_coNrQOcarOUSZQo8HOioaImlMd9JJcAg.JPEG/11.JPG?type=w773" data-lazy-src="" data-width="693" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-ae0dc305-e60a-498a-8ccb-8cbcfabec539_0">
                                    </a>
                                </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-ae0dc305-e60a-498a-8ccb-8cbcfabec539&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot; }}"></script>
                </div>
                <div class="se-component se-image se-l-default __se-component" id="SE-7270a6c5-e61c-4c1d-8393-9508fb6dca46">
                    <div class="se-component-content se-component-content-fit">
                        <div class="se-section se-section-image se-l-default se-section-align-center">
                                <div class="se-module se-module-image" style="">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-7270a6c5-e61c-4c1d-8393-9508fb6dca46&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfMTA3/MDAxNzUwMDA0NjU2MzMy.F2HMTPjFNJV3vp6L-_RaF3hzN1LfQOkJAI846rd6fZkg.CZmun3dp5nhgn8Cj4WLCrxubdaMV5AYitkjrh2-fCS8g.JPEG/12.JPG&quot;, &quot;originalWidth&quot; : &quot;4032&quot;, &quot;originalHeight&quot; : &quot;3024&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfMTA3/MDAxNzUwMDA0NjU2MzMy.F2HMTPjFNJV3vp6L-_RaF3hzN1LfQOkJAI846rd6fZkg.CZmun3dp5nhgn8Cj4WLCrxubdaMV5AYitkjrh2-fCS8g.JPEG/12.JPG?type=w773" data-lazy-src="" data-width="693" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-7270a6c5-e61c-4c1d-8393-9508fb6dca46_0">
                                    </a>
                                </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-7270a6c5-e61c-4c1d-8393-9508fb6dca46&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot; }}"></script>
                </div>
                <div class="se-component se-text se-l-default" id="SE-756c5653-16ef-41a0-8346-41e0c7fbab87">
                    <div class="se-component-content">
                        <div class="se-section se-section-text se-l-default">
                            <div class="se-module se-module-text">
                                    <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-0149d601-17d3-4361-b76d-3c22964bbd53"><span style="" class="se-fs- se-ff-   " id="SE-094e4e31-4a49-11f0-9028-1722ee0ca302">비빔밥 안에 들어가는 나물도</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-54beb409-6680-4ae2-88df-1bf3d5f48d92"><span style="" class="se-fs- se-ff-   " id="SE-094e7542-4a49-11f0-9028-c79797cd9f0d">건나물, 생야채, 표고버섯, </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-d4e77be0-41be-42b4-b061-f2779ab3ca6f"><span style="" class="se-fs- se-ff-   " id="SE-094e7543-4a49-11f0-9028-1de98938a4b1">도라지, 고사리 등 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-a1afd37e-79aa-4cf2-be52-abf73f71c93e"><span style="" class="se-fs- se-ff-   " id="SE-094e7544-4a49-11f0-9028-edcff821d338">제철에 맞춰 엄선된 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-ccabb87b-7c7c-4ca9-9a2f-87af3566ff48"><span style="" class="se-fs- se-ff-   " id="SE-094e7545-4a49-11f0-9028-039df2440eb3">나물들이 들어가는데, </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-d528311c-5e04-4ccb-b2aa-593d8f28f139"><span style="" class="se-fs- se-ff-   " id="SE-094e7546-4a49-11f0-9028-bb1675d9ff0f">하나하나 다 본연의 맛이 좋았어요~</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-709ea15d-b8a8-4c4c-b4ce-983ced7ffc18"><span style="" class="se-fs- se-ff-   " id="SE-094e7547-4a49-11f0-9028-53598413be1c">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-6d828263-ad77-46f8-8781-5e2c8d324f76"><span style="" class="se-fs- se-ff-   " id="SE-094e7548-4a49-11f0-9028-93be6081c743">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-756c5653-16ef-41a0-8346-41e0c7fbab87&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                </div>                <div class="se-component se-image se-l-default __se-component" id="SE-c4047314-5c8a-45ea-b0f4-a3457f97dc08">
                    <div class="se-component-content se-component-content-fit">
                        <div class="se-section se-section-image se-l-default se-section-align-center">
                                <div class="se-module se-module-image" style="">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-c4047314-5c8a-45ea-b0f4-a3457f97dc08&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfMTIy/MDAxNzUwMDA0NjU3MTUw.ZS0NAagxeqVqRWXBm3GVWf8J2K8_gPdSQ1ru3Zh5uskg.PwppBxXqBkGc4-HKInYsC2vHVDJjAfkwoAhAadKcGDgg.JPEG/14.JPG&quot;, &quot;originalWidth&quot; : &quot;4032&quot;, &quot;originalHeight&quot; : &quot;3024&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfMTIy/MDAxNzUwMDA0NjU3MTUw.ZS0NAagxeqVqRWXBm3GVWf8J2K8_gPdSQ1ru3Zh5uskg.PwppBxXqBkGc4-HKInYsC2vHVDJjAfkwoAhAadKcGDgg.JPEG/14.JPG?type=w773" data-lazy-src="" data-width="693" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-c4047314-5c8a-45ea-b0f4-a3457f97dc08_0">
                                    </a>
                                </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_image&quot;, &quot;id&quot;: &quot;SE-c4047314-5c8a-45ea-b0f4-a3457f97dc08&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;image&quot; }}"></script>
                </div>
                <div class="se-component se-text se-l-default" id="SE-5fdcb089-690b-4b0e-a800-4e53849e2ef3">
                    <div class="se-component-content">
                        <div class="se-section se-section-text se-l-default">
                            <div class="se-module se-module-text">
                                    <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-ee322ecb-ea6e-4245-b33a-540c6bf56445"><span style="" class="se-fs- se-ff-   " id="SE-094e7549-4a49-11f0-9028-1d13b3edd6dc">삼광쌀로 지은 밥도 맛있더라구요~</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-ca6f2e89-0330-4988-86dd-e748cdf952ca"><span style="" class="se-fs- se-ff-   " id="SE-094e754a-4a49-11f0-9028-0f381d6d69d0">밥 한 숟가락에 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-da324d65-3ea5-4974-b628-c7b98403c6a7"><span style="" class="se-fs- se-ff-   " id="SE-094e754b-4a49-11f0-9028-5f7cad5dc4e2">입안이 꽉 차는 느낌이 넘 좋았어요!</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-ad1ea82f-20a6-4317-b526-e346fe25dcfd"><span style="" class="se-fs- se-ff-   " id="SE-094e754c-4a49-11f0-9028-a3c34e5978ce">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-5fdcb089-690b-4b0e-a800-4e53849e2ef3&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                </div>                <div class="se-component se-imageStrip se-imageStrip2 se-l-default __se-component" id="SE-f4cc0cb6-a5e4-44db-9ec2-c085d23b76ec">
                    <div class="se-component-content se-component-content-fit">
                        <div class="se-section se-section-imageStrip se-l-default">
                            <div class="se-imageStrip-container se-imageStrip-col-2">
                                <div class="se-module se-module-image" style="width:50.0%;">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-f9552ac0-e7ee-4b7c-a5a0-e01ca40e377e&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfMTY2/MDAxNzUwMDEwMTI1MTM0.uB773QxYzCtRc6H_8GM10T53IATbbEVzGft96vJh9okg.26NB8tMvUYiGCm3x1VUC5oSCvcsSM-aCLt4pbIIr4v8g.JPEG/9.JPG&quot;, &quot;originalWidth&quot; : &quot;4032&quot;, &quot;originalHeight&quot; : &quot;3024&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfMTY2/MDAxNzUwMDEwMTI1MTM0.uB773QxYzCtRc6H_8GM10T53IATbbEVzGft96vJh9okg.26NB8tMvUYiGCm3x1VUC5oSCvcsSM-aCLt4pbIIr4v8g.JPEG/9.JPG?type=w386" data-lazy-src="" data-width="693" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-f4cc0cb6-a5e4-44db-9ec2-c085d23b76ec_0">
                                    </a>
                                </div>
                                <div class="se-module se-module-image" style="width:50.0%;">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-8bc26231-fa2e-464d-9295-e71e535db713&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfMTY1/MDAxNzUwMDEwMTI1MTE0.b2ovMjDAgO_Fz7r2ohd_NnN8MYLgpShbIQu2RcmYAScg.6MRsgmLYaFpf8_0T27ZJEHU9uEKDVCC3CNDc_n0DzCsg.JPEG/10.JPG&quot;, &quot;originalWidth&quot; : &quot;4032&quot;, &quot;originalHeight&quot; : &quot;3024&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfMTY1/MDAxNzUwMDEwMTI1MTE0.b2ovMjDAgO_Fz7r2ohd_NnN8MYLgpShbIQu2RcmYAScg.6MRsgmLYaFpf8_0T27ZJEHU9uEKDVCC3CNDc_n0DzCsg.JPEG/10.JPG?type=w386" data-lazy-src="" data-width="693" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-f4cc0cb6-a5e4-44db-9ec2-c085d23b76ec_1">
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_imageStrip&quot;, &quot;id&quot;: &quot;SE-f4cc0cb6-a5e4-44db-9ec2-c085d23b76ec&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;imageStrip&quot;, &quot;images&quot;: [ {&quot;ctype&quot;: &quot;image&quot;, &quot;id&quot;: &quot;SE-f9552ac0-e7ee-4b7c-a5a0-e01ca40e377e&quot; } , {&quot;ctype&quot;: &quot;image&quot;, &quot;id&quot;: &quot;SE-8bc26231-fa2e-464d-9295-e71e535db713&quot; } ] }}"></script>
                </div>                <div class="se-component se-text se-l-default" id="SE-61432950-7be2-4c9c-be80-72a58d5e9823">
                    <div class="se-component-content">
                        <div class="se-section se-section-text se-l-default">
                            <div class="se-module se-module-text">
                                    <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-32f43826-1ef5-42f0-97b9-f65168f0a467"><span style="" class="se-fs- se-ff-   " id="SE-094e9c5d-4a49-11f0-9028-5d89d3f5156c">함께 주문하고 싶은 사이드 메뉴는 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-fe46e9f1-0435-4807-aa90-4ff347ee7e02"><span style="" class="se-fs- se-ff-   " id="SE-094e9c5e-4a49-11f0-9028-a7b1be401967">바로 치즈김치전!</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-f3ecc752-f899-45bf-bfbb-297ed5d2f9f2"><span style="" class="se-fs- se-ff-   " id="SE-094e9c5f-4a49-11f0-9028-278e15449fad">피자치즈와 모짜렐라가 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-506286db-13a5-49f6-b199-4791f595cd1b"><span style="" class="se-fs- se-ff-   " id="SE-094e9c60-4a49-11f0-9028-51292deb319e">가득 들어간 김치전인데, </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-4d0641ab-b660-4a76-80cd-94de9cc44886"><span style="" class="se-fs- se-ff-   " id="SE-094e9c61-4a49-11f0-9028-dbe704899462">겉은 바삭하고 속은 촉촉한 게 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-300fbcc5-dbbc-4083-ae25-854c1cf8f033"><span style="" class="se-fs- se-ff-   " id="SE-094e9c62-4a49-11f0-9028-3569d1dbf13d">비빔밥이랑 궁합 최고예요. </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-8f2a410c-04d0-4dc9-8f8e-291c7843fc8f"><span style="" class="se-fs- se-ff-   " id="SE-094e9c63-4a49-11f0-9028-8b1ccced3ca0">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-61432950-7be2-4c9c-be80-72a58d5e9823&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                </div>                <div class="se-component se-imageStrip se-imageStrip2 se-l-default __se-component" id="SE-7bdf866f-ad3f-4b4b-ac2c-6aaf46fa0070">
                    <div class="se-component-content se-component-content-fit">
                        <div class="se-section se-section-imageStrip se-l-default">
                            <div class="se-imageStrip-container se-imageStrip-col-2">
                                <div class="se-module se-module-image" style="width:50.0%;">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-e0b4343a-4428-4aef-9c50-155bd92a7b87&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfNzkg/MDAxNzUwMDEwMTI1MTk5.J2Qp8YA-Hk8vIMnIhCH9ORFDRgtFyXgLRX2ojRjsyGAg.8wu0DuwAjAOlMCLE5jDl81dupbTF9_aSgY5WIAbatjkg.JPEG/6.JPG&quot;, &quot;originalWidth&quot; : &quot;4032&quot;, &quot;originalHeight&quot; : &quot;3024&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfNzkg/MDAxNzUwMDEwMTI1MTk5.J2Qp8YA-Hk8vIMnIhCH9ORFDRgtFyXgLRX2ojRjsyGAg.8wu0DuwAjAOlMCLE5jDl81dupbTF9_aSgY5WIAbatjkg.JPEG/6.JPG?type=w386" data-lazy-src="" data-width="693" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-7bdf866f-ad3f-4b4b-ac2c-6aaf46fa0070_0">
                                    </a>
                                </div>
                                <div class="se-module se-module-image" style="width:50.0%;">
                                    <a class="se-module-image-link __se_image_link __se_link" style="" onclick="return false;" data-linktype="img" data-linkdata="{&quot;id&quot; : &quot;SE-187fd201-260d-45a9-bb2b-034d4cfe8904&quot;, &quot;src&quot; : &quot;https://postfiles.pstatic.net/MjAyNTA2MTZfNTUg/MDAxNzUwMDEwMTI1MTAy.6IEewhchJMCB5SfwZK-NXgy8QA9QafHDuwKSMlpp8Nog.EIc5ErWxcExhWuwTjyIp1sJe903B1CPPPFdI0m8Q6XMg.JPEG/8.JPG&quot;, &quot;originalWidth&quot; : &quot;4032&quot;, &quot;originalHeight&quot; : &quot;3024&quot;, &quot;linkUse&quot; : &quot;false&quot;, &quot;link&quot; : &quot;&quot;}" area-hidden="true">
                                        <img src="https://postfiles.pstatic.net/MjAyNTA2MTZfNTUg/MDAxNzUwMDEwMTI1MTAy.6IEewhchJMCB5SfwZK-NXgy8QA9QafHDuwKSMlpp8Nog.EIc5ErWxcExhWuwTjyIp1sJe903B1CPPPFdI0m8Q6XMg.JPEG/8.JPG?type=w386" data-lazy-src="" data-width="693" data-height="519" alt="" class="se-image-resource egjs-visible" id="SE-7bdf866f-ad3f-4b4b-ac2c-6aaf46fa0070_1">
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_imageStrip&quot;, &quot;id&quot;: &quot;SE-7bdf866f-ad3f-4b4b-ac2c-6aaf46fa0070&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;imageStrip&quot;, &quot;images&quot;: [ {&quot;ctype&quot;: &quot;image&quot;, &quot;id&quot;: &quot;SE-e0b4343a-4428-4aef-9c50-155bd92a7b87&quot; } , {&quot;ctype&quot;: &quot;image&quot;, &quot;id&quot;: &quot;SE-187fd201-260d-45a9-bb2b-034d4cfe8904&quot; } ] }}"></script>
                </div>                <div class="se-component se-text se-l-default" id="SE-fd3f8574-2894-4ae2-8fdf-2ff79f2b0277">
                    <div class="se-component-content">
                        <div class="se-section se-section-text se-l-default">
                            <div class="se-module se-module-text">
                                    <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-754c52ef-5d36-453f-b2df-08800cb994a1"><span style="" class="se-fs- se-ff-   " id="SE-094e9c64-4a49-11f0-9028-dff9c8c48fd2">술 한잔 곁들이고 싶다면, </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-4f638f22-619e-4961-8d10-b2aae92a3617"><span style="" class="se-fs- se-ff-   " id="SE-094e9c65-4a49-11f0-9028-27760339d64b">비빔밥 전용 막걸리도 있어요.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-6f75632a-058d-4131-9b28-224de7a1d7c3"><span style="" class="se-fs- se-ff-   " id="SE-094e9c66-4a49-11f0-9028-3317a1ecc101">‘한 잔 막걸리’라는 이름답게 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-4d2f1044-d419-4da3-9cb7-34259ff8bf30"><span style="" class="se-fs- se-ff-   " id="SE-094e9c67-4a49-11f0-9028-83a1f3d039f2">식전–식중–식후로 나눠 마시는 재미가 있어요. </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-a8b03f69-ebca-4370-a881-e67c7b740ab2"><span style="" class="se-fs- se-ff-   " id="SE-094e9c68-4a49-11f0-9028-f1c425430151">과일향도 은은하고, </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-ab39c512-1756-42fc-9ed6-33f883b9498a"><span style="" class="se-fs- se-ff-   " id="SE-094e9c69-4a49-11f0-9028-3367e9427dcb">단맛과 신맛이 균형 잡혀 있어서 </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-24029fe4-897b-4464-95e9-abae83cb5c85"><span style="" class="se-fs- se-ff-   " id="SE-094e9c6a-4a49-11f0-9028-9b2141cfb222">비빔밥과 찰떡이에요.</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-7bd6f548-6498-43ba-a9d3-7b69b853e3c6"><span style="" class="se-fs- se-ff-   " id="SE-094e9c6b-4a49-11f0-9028-53e0f77493e8">&ZeroWidthSpace;</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-09af499c-1630-4ddf-8401-e9820b971001"><span style="" class="se-fs- se-ff-   " id="SE-094e9c6c-4a49-11f0-9028-45c1c98416a3">남산 산책하다가, </span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-0410fdd2-adf2-4b43-86dd-0cce5b5a87a8"><span style="" class="se-fs- se-ff-   " id="SE-094e9c6d-4a49-11f0-9028-f9c924127542">혹은 명동역 근처로</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-fd515e10-acde-43e4-bfcf-f00371acddbf"><span style="" class="se-fs- se-ff-   " id="SE-094e9c6e-4a49-11f0-9028-0931d7067c2f">들리기 좋은 곳이랍니다^^</span></p><!-- } SE-TEXT --><!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align-center " style="" id="SE-c269114f-3ed7-4aa3-ac6a-07a163ffb7f8"><span style="" class="se-fs- se-ff-   " id="SE-094e9c6f-4a49-11f0-9028-554e7b073831">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-fd3f8574-2894-4ae2-8fdf-2ff79f2b0277&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                </div>                <div class="se-component se-placesMap se-l-default __se-component" id="SE-c3fb8301-d99c-4aec-a64a-889bd5144d63">
                    <div class="se-component-content">
                        <div class="se-section se-section-placesMap  se-section-align-center se-l-default">
                            <div class="se-module se-module-map-image" style="padding-top: 45%;"><div class="__se_map se-dynamic-map" tabindex="0" style="position: relative; overflow: hidden; background: rgb(248, 249, 250);"><div style="position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; overflow: visible; width: 100%; height: 100%; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); z-index: 0; cursor: url(&quot;https://ssl.pstatic.net/static/maps/mantle/2x/openhand.cur&quot;), default;"><div style="position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; overflow: visible; width: 100%; height: 100%; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); z-index: 0;"><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 1;"><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: none; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 0; user-select: none;"></div><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 1; user-select: none;"><div style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 0px; height: 0px; overflow: visible; box-sizing: content-box !important;"><div draggable="false" unselectable="on" style="position: absolute; top: -44px; left: 209px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111770/50761@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 212px; left: 209px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111770/50762@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -300px; left: 209px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111770/50760@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -300px; left: 465px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111771/50760@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 212px; left: -47px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111769/50762@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -44px; left: 465px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111771/50761@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -44px; left: -47px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111769/50761@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 212px; left: 465px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111771/50762@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -300px; left: -47px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111769/50760@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -300px; left: 721px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111772/50760@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 212px; left: -303px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111768/50762@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -44px; left: 721px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111772/50761@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -44px; left: -303px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111768/50761@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: 212px; left: 721px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111772/50762@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div><div draggable="false" unselectable="on" style="position: absolute; top: -300px; left: -303px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; opacity: 1; width: 256px; height: 256px;"><img draggable="false" unselectable="on" alt="" crossorigin="anonymous" width="256" height="256" src="https://map.pstatic.net/nrb/styles/basic/1749778822/17/111768/50760@2x.png?mt=bg.ol.sw.ar.lko" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; opacity: 1; position: absolute; left: 0px; top: 0px; z-index: 0; width: 256px; height: 256px;"></div></div></div><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 100;"><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 101;"></div><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 103;"><div title="" style="position: absolute; overflow: hidden; box-sizing: content-box !important; cursor: inherit; left: 331px; top: 116px; width: 32px; height: 42px;"><img draggable="false" unselectable="on" src="https://editor-static.pstatic.net/c/resources/common/img/common-icon-places-marker-x2-20180920.png" alt="" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; user-select: none; -webkit-user-drag: none; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important; position: absolute; cursor: pointer; width: 32px; height: 42px; left: 0px; top: 0px;"></div></div><div style="overflow: visible; width: 100%; height: 0px; position: absolute; display: block; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; z-index: 106;"></div></div></div><div style="position: absolute; display: none; margin: 0px; padding: 0px; border: 0px none; top: 0px; left: 0px; overflow: visible; width: 100%; height: 100%; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); background-color: rgb(255, 255, 255); z-index: 10000; opacity: 0.5;"></div></div></div><div style="position: absolute; z-index: 100; margin: 0px; padding: 0px; pointer-events: none; bottom: 0px; right: 0px;"><div style="border: 0px none; margin: 0px; padding: 0px; pointer-events: none; float: right; height: 20px;"><div style="position: relative; width: 53px; height: 14px; margin: 0px 12px 6px 2px; overflow: hidden; pointer-events: auto;"><span style="display: block; margin: 0px; padding: 0px 4px; text-align: center; font-size: 10px; line-height: 11px; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; font-weight: 700; color: rgb(34, 34, 37); text-shadow: rgba(255, 255, 255, 0.8) -1px 0px, rgba(255, 255, 255, 0.8) 0px 1px, rgba(255, 255, 255, 0.8) 1px 0px, rgba(255, 255, 255, 0.8) 0px -1px;">50m</span><img src="https://ssl.pstatic.net/static/maps/mantle/2x/new-scale-normal-b.png" width="47" height="3" alt="" style="position: absolute; left: 3px; bottom: 0px; z-index: 2; display: block; width: 47px; height: 3px; overflow: hidden; margin: 0px; padding: 0px; border: 0px none; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/new-scale-normal-l.png" width="3" height="8" alt="" style="position:absolute;left:0;bottom:0;z-index:2;display:block;width:3px;height:8px;overflow:hidden;margin:0;padding:0;border:0 none;max-width:none !important;max-height:none !important;min-width:0 !important;min-height:0 !important;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/new-scale-normal-r.png" width="3" height="8" alt="" style="position:absolute;right:0;bottom:0;z-index:2;display:block;width:3px;height:8px;overflow:hidden;margin:0;padding:0;border:0 none;max-width:none !important;max-height:none !important;min-width:0 !important;min-height:0 !important;"></div></div></div><div style="position: absolute; z-index: 100; margin: 0px; padding: 0px; pointer-events: none; bottom: 0px; left: 0px;"><div style="border: 0px none; margin: 0px; padding: 0px; pointer-events: none; float: left; height: 21px;"><div class="map_copyright" style="margin: 0px; padding: 0px 0px 2px 10px; height: 19px; line-height: 19px; color: rgb(68, 68, 68); font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; font-size: 11px; clear: both; white-space: nowrap; pointer-events: none;"><div style="float: left;"><span style="white-space: pre; color: rgb(68, 68, 68);">© NAVER Corp.</span></div><a href="#" style="font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; font-size: 11px; line-height: 19px; margin: 0px 0px 0px 5px; padding: 0px; color: rgb(68, 68, 68); float: left; pointer-events: auto; text-decoration: underline; display: none;">더보기</a><div style="float: left;"><a target="_blank" href="http://www.openstreetmap.org/copyright" style="pointer-events: auto; white-space: pre; display: none; color: rgb(68, 68, 68);"> /OpenStreetMap</a></div></div></div></div><div style="border: 1px solid rgb(41, 41, 48); background: rgb(255, 255, 255); padding: 15px; color: rgb(51, 51, 51); position: absolute; font-size: 11px; line-height: 1.5; clear: both; display: none; max-width: 350px !important; max-height: 300px !important;"><h5 style="font-size: 12px; margin-top: 0px; margin-bottom: 10px;">지도 데이터</h5><a href="#" style="position: absolute; top: 8px; right: 8px; width: 14px; height: 14px; font-size: 14px; line-height: 14px; display: block; overflow: hidden; color: rgb(68, 68, 68); text-decoration: none; font-weight: bold; text-align: center;">x</a><div><span style="white-space: pre; color: rgb(68, 68, 68); float: left;">© NAVER Corp.</span><a target="_blank" href="http://www.openstreetmap.org/copyright" style="pointer-events: auto; white-space: pre; color: rgb(68, 68, 68); float: left; display: none;"> /OpenStreetMap</a></div></div><div style="position: absolute; z-index: 100; margin: 0px; padding: 0px; pointer-events: none; top: 0px; right: 0px;"><div style="border: 0px none; margin: 0px; padding: 0px; pointer-events: none; float: right;"><div style="position: relative; z-index: 3; pointer-events: auto;"><div style="position: relative; z-index: 0; width: 28px; margin: 10px; border: 1px solid rgb(68, 68, 68); box-sizing: content-box !important; user-select: none;"><a href="#" style="position: relative; z-index: 2; width: 28px; height: 28px; cursor: pointer; display: block; overflow: hidden; border-bottom: 0px none; box-sizing: content-box !important;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-in-small-normal.png" width="28" height="28" alt="지도 확대" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 28px; height: 28px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"></a><div style="position: relative; width: 28px; height: 216px; overflow: hidden; margin: 0px; padding: 7px 0px; background-color: rgb(255, 255, 255); cursor: pointer; box-sizing: content-box !important; display: none;"><div style="position: absolute; top: 7px; bottom: 7px; left: 12px; width: 4px; height: 216px; display: block; background-color: rgb(47, 135, 236);"></div><div style="position: absolute; top: 7px; bottom: 7px; left: 12px; width: 4px; height: 44px; display: block; background-color: rgb(202, 205, 209);"></div><a href="#" style="position: absolute; left: 4px; width: 18px; height: 10px; top: 44px; border: 1px solid rgb(68, 68, 68); cursor: move; display: block; overflow: hidden; box-sizing: content-box !important;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-handle.png" width="18" height="10" alt="지도 확대/축소 슬라이더" style="margin:0;padding:0;border:solid 0 transparent;display:block;box-sizing:content-box !important;max-width:none !important;max-height:none !important;min-width:0 !important;min-height:0 !important;width:18px;height:10px;"></a></div><a href="#" style="position: relative; z-index: 2; width: 28px; height: 28px; cursor: pointer; display: block; overflow: hidden; border-top: 1px solid rgb(202, 205, 209); box-sizing: content-box !important;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-out-small-normal.png" width="28" height="28" alt="지도 축소" style="margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 28px; height: 28px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"></a><div style="position: absolute; top: 22px; width: 44px; height: 0px; overflow: visible; display: none; left: -51px;"><div style="display: block; margin: 0px; padding: 0px;"><h4 style="visibility:hidden;width:0;height:0;overflow:hidden;margin:0;padding:0;">지도 컨트롤러 범례</h4><div style="position: absolute; top: 43px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-on.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">부동산</span></div><div style="position: absolute; top: 63px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-normal.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">거리</span></div><div style="position: absolute; top: 83px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-normal.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">읍,면,동</span></div><div style="position: absolute; top: 113px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-normal.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">시,군,구</span></div><div style="position: absolute; top: 143px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-normal.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">시,도</span></div><div style="position: absolute; top: 163px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; overflow: hidden; box-sizing: content-box !important; visibility: visible;"><img src="https://ssl.pstatic.net/static/maps/mantle/2x/zoom-legend-left-normal.png" alt="" style="position: absolute; top: 0px; left: 0px; z-index: 0; margin: 0px; padding: 0px; border: 0px solid transparent; display: block; width: 44px; height: 17px; box-sizing: content-box !important; max-width: none !important; max-height: none !important; min-width: 0px !important; min-height: 0px !important;"><span style="margin: 0px; border: 0px solid transparent; display: block; font-family: Helvetica, AppleSDGothicNeo-Light, nanumgothic, NanumGothic, 나눔고딕, Dotum, 돋움, sans-serif; position: relative; z-index: 2; line-height: 17px; color: rgb(255, 255, 255); font-size: 11px; padding: 0px 4px 0px 0px; text-align: center; letter-spacing: -1px; box-sizing: content-box !important;">국가</span></div></div></div></div></div></div></div></div>
                                <img src="https://simg.pstatic.net/static.map/v2/map/staticmap.bin?caller=smarteditor&amp;markers=size%3Amid%7Ccolor%3A0x11cc73%7Ctype%3Ad%7CviewSizeRatio%3A0.7%7Cpos%3A126.9869447%2037.5581107&amp;w=700&amp;h=315&amp;scale=2&amp;dataversion=174.22" alt="" class="se-map-image egjs-visible" style="display: none;">
                            </div>
                                <div class="se-module se-module-map-text ">
                                        <a href="#" target="_blank" class="se-map-info __se_link" onclick="return false;" data-linktype="map" data-linkdata="{&quot;eventTarget&quot; : &quot;placeDesc&quot;, &quot;placeId&quot; : &quot;13573290&quot;, &quot;searchEngine&quot; : &quot;naver&quot;, &quot;searchType&quot; : &quot;s&quot;, &quot;name&quot; : &quot;목멱산방&quot;, &quot;address&quot; : &quot;서울특별시 중구 퇴계로20길 71 1층 목멱산방&quot;, &quot;latitude&quot; : &quot;37.5581107&quot;, &quot;longitude&quot; : &quot;126.9869447&quot;, &quot;tel&quot; : &quot;02-318-4790&quot;, &quot;bookingUrl&quot; : null }">
                                        <strong class="se-map-title">목멱산방</strong>
                                        <p class="se-map-address">서울특별시 중구 퇴계로20길 71 1층 목멱산방</p>
                                    </a>
                                </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module="{&quot;type&quot;:&quot;v2_map&quot;, &quot;id&quot; :&quot;SE-c3fb8301-d99c-4aec-a64a-889bd5144d63&quot;, &quot;data&quot; : { &quot;layout&quot;: &quot;default&quot;, &quot;searchEngine&quot; : &quot;naver&quot;, &quot;places&quot; : [{&quot;placeId&quot;:&quot;13573290&quot;,&quot;name&quot;:&quot;목멱산방&quot;,&quot;address&quot;:&quot;서울특별시 중구 퇴계로20길 71 1층 목멱산방&quot;,&quot;latlng&quot;:{&quot;@ctype&quot;:&quot;position&quot;,&quot;latitude&quot;:37.5581107,&quot;longitude&quot;:126.9869447},&quot;searchType&quot;:&quot;s&quot;,&quot;tel&quot;:&quot;02-318-4790&quot;,&quot;bookingUrl&quot;:null}] }}" data-module-v2="{&quot;type&quot;:&quot;v2_map&quot;, &quot;id&quot; :&quot;SE-c3fb8301-d99c-4aec-a64a-889bd5144d63&quot;, &quot;data&quot; : { &quot;layout&quot;: &quot;default&quot;, &quot;searchEngine&quot; : &quot;naver&quot;, &quot;places&quot; : [{&quot;placeId&quot;:&quot;13573290&quot;,&quot;name&quot;:&quot;목멱산방&quot;,&quot;address&quot;:&quot;서울특별시 중구 퇴계로20길 71 1층 목멱산방&quot;,&quot;latlng&quot;:{&quot;@ctype&quot;:&quot;position&quot;,&quot;latitude&quot;:37.5581107,&quot;longitude&quot;:126.9869447},&quot;searchType&quot;:&quot;s&quot;,&quot;tel&quot;:&quot;02-318-4790&quot;,&quot;bookingUrl&quot;:null}] }}"></script>
                </div>                <div class="se-component se-text se-l-default" id="SE-ec0a8e92-f1da-4dd2-8e82-db0bb01925d2">
                    <div class="se-component-content">
                        <div class="se-section se-section-text se-l-default">
                            <div class="se-module se-module-text">
                                    <!-- SE-TEXT { --><p class="se-text-paragraph se-text-paragraph-align- " style="" id="SE-8161de76-0f29-4c0e-ae4e-5149143aef27"><span style="" class="se-fs- se-ff-   " id="SE-094ec380-4a49-11f0-9028-875af54a0f41">&ZeroWidthSpace;</span></p><!-- } SE-TEXT -->
                            </div>
                        </div>
                    </div>
                    <script type="text/data" class="__se_module_data" data-module-v2="{&quot;type&quot;: &quot;v2_text&quot;, &quot;id&quot;: &quot;SE-ec0a8e92-f1da-4dd2-8e82-db0bb01925d2&quot;, &quot;data&quot;: {&quot;ctype&quot;: &quot;text&quot;  }}"></script>
                </div>    <div class="ssp-adcontent align_center"><div id="ssp-adcontent" class="ssp_adcontent_inner"><div style="width: 100%; height: auto; margin: 0px auto; line-height: 0;"><iframe id="ssp-adcontent_tgtLREC" frameborder="no" scrolling="no" tabindex="0" name="" title="AD" style="width: 100%; height: 211px; visibility: inherit; border: 0px; vertical-align: bottom;"></iframe></div></div></div></div>""",
                "title": "목멱산방",
                "summary": "한식 맛집 홍보"
            }
        ]
        # 인스타 글 예시
        self.insta_example = [
            {
                "caption": """힘든 월요일 잘 이겨내신 여러분~~~
                            소나기도 내리고 힘드셨을텐데
                            오늘 하루 고생 많으셨어요~~^^
                            고생한 나를 위해 시원한 맥주에
                            낙곱새~~기가 막히죠??낙지에 대창올리고
                            그 위에 새우~화룡점정으로 생와사비~
                            그 맛은 뭐 말씀 안드려도 여러분들이
                            더 잘 아실거예요~~그럼 다들 낙곱새 고고~~""",
                "title": "국민 낙곱새",
                "summary": "낙곱새 맛집 홍보"
             },
            {
                "caption": """안녕하세요! 타코몰리김포점입니다!
                                타코몰리는 멕시코 문화와 풍부한맛을 경험할 수 있는 특별한 공간입니다.🎉
                                
                                🌶 대표 메뉴를 맛보세요
                                수제 타코, 바삭한 퀘사디아, 풍성한 부리또로 다양한 맛을 즐길 수 있습니다.
                                
                                📸 특별한 순간을 담아보세요
                                #타코몰리김포 해시태그와 함께 여러분의 멋진 사진을 공유해주세요.
                                이벤트가 기다리고 있답니다!!
                                (새우링/치즈스틱/음료 택1)
                                
                                📍 위치
                                김포한강 11로 140번길 15-2
                                
                                멕시코의 맛과 전통에 푹 빠져보세요!
                                언제든지 여러분을 기다리고 있겠습니다🌟""",
                "title": "타코몰리",
                "summary": "멕시칸 맛집 홍보"
            },
            {
                "caption":"""📣명륜진사갈비 신메뉴 3종 출시!

                            특제 고추장 양념에 마늘과 청양고추를 더해
                            매콤한 불맛이 일품인 #매콤불고기 🌶️
                            
                            특제 간장 양념에 마늘과 청양고추를 더해
                            달콤한 감칠맛이 있는 #달콤불고기 🍯
                            
                            갈비뼈에 붙어있는 부위로 일반 삼겹살보다
                            더욱 깊은 맛과 풍미를 가진 #삼겹갈비 까지🍖
                            
                            신메뉴로 더욱 풍성해진 명륜진사갈비에서
                            연말 가족/단체모임을 즐겨보세요!
                            
                            ※ 신메뉴는 지점에 따라 탄력적으로 운영되고 있으니,
                            자세한 문의는 방문하실 매장으로 확인 부탁드립니다.""",
                "title": "명륜진사갈비",
                "summary": "갈비 맛집 홍보"
            }
        ]
        
        # 플랫폼별 콘텐츠 특성 정의 (대폭 개선)
        self.platform_specs = {
            '인스타그램': {
                'max_length': 2200,
                'hashtag_count': 15,
                'style': '감성적이고 시각적',
                'format': '짧은 문장, 해시태그 활용',
                'content_structure': '후킹 문장 → 스토리텔링 → 행동 유도 → 해시태그',
                'writing_tips': [
                    '첫 문장으로 관심 끌기',
                    '이모티콘을 적절히 활용',
                    '줄바꿈으로 가독성 높이기',
                    '개성 있는 말투 사용',
                    '팔로워와의 소통 유도'
                ],
                'hashtag_strategy': [
                    '브랜딩 해시태그 포함',
                    '지역 기반 해시태그',
                    '트렌딩 해시태그 활용',
                    '음식 관련 인기 해시태그',
                    '감정 표현 해시태그'
                ],
                'call_to_action': ['팔로우', '댓글', '저장', '공유', '방문']
            },
            '네이버 블로그': {
                'max_length': 3000,
                'hashtag_count': 10,
                'style': '정보성과 친근함',
                'format': '구조화된 내용, 상세 설명',
                'content_structure': '제목 → 인트로 → 본문(구조화) → 마무리',
                'writing_tips': [
                    '검색 키워드 자연스럽게 포함',
                    '단락별로 소제목 활용',
                    '구체적인 정보 제공',
                    '후기/리뷰 형식 활용',
                    '지역 정보 상세히 기술'
                ],
                'seo_keywords': [
                    '맛집', '리뷰', '추천', '후기',
                    '메뉴', '가격', '위치', '분위기',
                    '데이트', '모임', '가족', '혼밥'
                ],
                'call_to_action': ['방문', '예약', '문의', '공감', '이웃추가'],
                'image_placement_strategy': [
                    '매장 외관 → 인테리어 → 메뉴판 → 음식 → 분위기',
                    ##'텍스트 2-3문장마다 이미지 배치',
                    '이미지 설명은 간결하고 매력적으로',
                    '마지막에 대표 이미지로 마무리'
                ]
            }
        }

        # 톤앤매너별 스타일 (플랫폼별 세분화)
        # self.tone_styles = {
        #     '친근한': {
        #         '인스타그램': '반말, 친구같은 느낌, 이모티콘 많이 사용',
        #         '네이버 블로그': '존댓말이지만 따뜻하고 친근한 어조'
        #     },
        #     '정중한': {
        #         '인스타그램': '정중하지만 접근하기 쉬운 어조',
        #         '네이버 블로그': '격식 있고 신뢰감 있는 리뷰 스타일'
        #     },
        #     '재미있는': {
        #         '인스타그램': '유머러스하고 트렌디한 표현',
        #         '네이버 블로그': '재미있는 에피소드가 포함된 후기'
        #     },
        #     '전문적인': {
        #         '인스타그램': '전문성을 어필하되 딱딱하지 않게',
        #         '네이버 블로그': '전문가 관점의 상세한 분석과 평가'
        #     }
        # }

        # 카테고리별 플랫폼 특화 키워드
        self.category_keywords = {
            '음식': {
                '인스타그램': ['#맛스타그램', '#음식스타그램', '#먹스타그램', '#맛집', '#foodstagram'],
                '네이버 블로그': ['맛집 리뷰', '음식 후기', '메뉴 추천', '맛집 탐방', '식당 정보']
            },
            '매장': {
                '인스타그램': ['#카페스타그램', '#인테리어', '#분위기맛집', '#데이트장소'],
                '네이버 블로그': ['카페 추천', '분위기 좋은 곳', '인테리어 구경', '모임장소']
            },
            '이벤트': {
                '인스타그램': ['#이벤트', '#프로모션', '#할인', '#특가'],
                '네이버 블로그': ['이벤트 소식', '할인 정보', '프로모션 안내', '특별 혜택']
            }
        }

        # 감정 강도별 표현
        # self.emotion_levels = {
        #     '약함': '은은하고 차분한 표현',
        #     '보통': '적당히 활기찬 표현',
        #     '강함': '매우 열정적이고 강렬한 표현'
        # }

        # 이미지 타입 분류를 위한 키워드
        self.image_type_keywords = {
            '매장외관': ['외관', '건물', '간판', '입구', '외부'],
            '인테리어': ['내부', '인테리어', '좌석', '테이블', '분위기', '장식'],
            '메뉴판': ['메뉴', '가격', '메뉴판', '메뉴보드', 'menu'],
            '음식': ['음식', '요리', '메뉴', '디저트', '음료', '플레이팅'],
            '사람': ['사람', '고객', '직원', '사장', '요리사'],
            '기타': ['기타', '일반', '전체']
        }

    def generate_sns_content(self, request: SnsContentGetRequest) -> Dict[str, Any]:
        """
        SNS 콘텐츠 생성 (플랫폼별 특화)
        """
        try:
            # 이미지 다운로드 및 분석
            image_analysis = self._analyze_images_from_urls(request.images)

            # 네이버 블로그인 경우 이미지 배치 계획 생성
            image_placement_plan = None
            if request.platform == '네이버 블로그':
                image_placement_plan = self._create_image_placement_plan(image_analysis, request)

            # 플랫폼별 특화 프롬프트 생성
            prompt = self._create_platform_specific_prompt(request, image_analysis, image_placement_plan)

            # blog_example을 프롬프트에 추가
            if request.platform == '네이버 블로그' and hasattr(self, 'blog_example') and self.blog_example:
                prompt += f"\n\n**참고 예시:**\n{str(self.blog_example)}\n위 예시를 참고하여 점주의 입장에서 가게 홍보 게시물을 작성해주세요."
            elif hasattr(self, 'insta_example') and self.insta_example :
                prompt += f"\n\n**참고 예시:**\n{str(self.insta_example)}\n위 예시를 참고하여 점주의 입장에서 가게 홍보 게시물을 작성해주세요."

            # AI로 콘텐츠 생성
            generated_content = self.ai_client.generate_text(prompt, max_tokens=1500)

            # 플랫폼별 후처리
            processed_content = self._post_process_content(generated_content, request)

            # HTML 형식으로 포맷팅
            html_content = self._format_to_html(processed_content, request, image_placement_plan)

            result = {
                'success': True,
                'content': html_content
            }

            # 네이버 블로그인 경우 이미지 배치 가이드라인 추가
            if request.platform == '네이버 블로그' and image_placement_plan:
                result['image_placement_guide'] = image_placement_plan

            return result

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _analyze_images_from_urls(self, image_urls: list) -> Dict[str, Any]:
        """
        URL에서 이미지를 다운로드하고 분석 (이미지 타입 분류 추가)
        """
        analysis_results = []
        temp_files = []

        try:
            for i, image_url in enumerate(image_urls):
                # 이미지 다운로드
                temp_path = self.ai_client.download_image_from_url(image_url)
                if temp_path:
                    temp_files.append(temp_path)

                    # 이미지 분석
                    try:
                        image_info = self.image_processor.get_image_info(temp_path)
                        image_description = self.ai_client.analyze_image(temp_path)

                        # 이미지 타입 분류
                        image_type = self._classify_image_type(image_description)

                        analysis_results.append({
                            'index': i,
                            'url': image_url,
                            'info': image_info,
                            'description': image_description,
                            'type': image_type
                        })
                    except Exception as e:
                        analysis_results.append({
                            'index': i,
                            'url': image_url,
                            'error': str(e),
                            'type': '기타'
                        })

            return {
                'total_images': len(image_urls),
                'results': analysis_results
            }

        finally:
            # 임시 파일 정리
            for temp_file in temp_files:
                try:
                    os.remove(temp_file)
                except:
                    pass

    def _classify_image_type(self, description: str) -> str:
        """
        이미지 설명을 바탕으로 이미지 타입 분류
        """
        description_lower = description.lower()

        for image_type, keywords in self.image_type_keywords.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return image_type

        return '기타'

    def _create_image_placement_plan(self, image_analysis: Dict[str, Any], request: SnsContentGetRequest) -> Dict[
        str, Any]:
        """
        네이버 블로그용 이미지 배치 계획 생성
        """
        images = image_analysis.get('results', [])
        if not images:
            return None

        # 이미지 타입별 분류
        categorized_images = {
            '매장외관': [],
            '인테리어': [],
            '메뉴판': [],
            '음식': [],
            '사람': [],
            '기타': []
        }

        for img in images:
            img_type = img.get('type', '기타')
            categorized_images[img_type].append(img)

        # 블로그 구조에 따른 이미지 배치 계획
        placement_plan = {
            'structure': [
                {
                    'section': '인트로',
                    'description': '첫인상과 방문 동기',
                    'recommended_images': [],
                    'placement_guide': '매장 외관이나 대표적인 음식 사진으로 시작'
                },
                {
                    'section': '매장 정보',
                    'description': '위치, 분위기, 인테리어 소개',
                    'recommended_images': [],
                    'placement_guide': '매장 외관 → 내부 인테리어 순서로 배치'
                },
                {
                    'section': '메뉴 소개',
                    'description': '주문한 메뉴와 상세 후기',
                    'recommended_images': [],
                    'placement_guide': '메뉴판 → 실제 음식 사진 순서로 배치'
                },
                {
                    'section': '총평',
                    'description': '재방문 의향과 추천 이유',
                    'recommended_images': [],
                    'placement_guide': '가장 매력적인 음식 사진이나 전체 분위기 사진'
                }
            ],
            'image_sequence': [],
            'usage_guide': []
        }

        # 각 섹션에 적절한 이미지 배정
        # 인트로: 매장외관 또는 대표 음식
        if categorized_images['매장외관']:
            placement_plan['structure'][0]['recommended_images'].extend(categorized_images['매장외관'][:1])
        elif categorized_images['음식']:
            placement_plan['structure'][0]['recommended_images'].extend(categorized_images['음식'][:1])

        # 매장 정보: 외관 + 인테리어
        placement_plan['structure'][1]['recommended_images'].extend(categorized_images['매장외관'])
        placement_plan['structure'][1]['recommended_images'].extend(categorized_images['인테리어'])

        # 메뉴 소개: 메뉴판 + 음식
        placement_plan['structure'][2]['recommended_images'].extend(categorized_images['메뉴판'])
        placement_plan['structure'][2]['recommended_images'].extend(categorized_images['음식'])

        # 총평: 남은 음식 사진 또는 기타
        remaining_food = [img for img in categorized_images['음식']
                          if img not in placement_plan['structure'][2]['recommended_images']]
        placement_plan['structure'][3]['recommended_images'].extend(remaining_food[:1])
        placement_plan['structure'][3]['recommended_images'].extend(categorized_images['기타'][:1])

        # 전체 이미지 순서 생성
        for section in placement_plan['structure']:
            for img in section['recommended_images']:
                if img not in placement_plan['image_sequence']:
                    placement_plan['image_sequence'].append(img)

        # 사용 가이드 생성
        placement_plan['usage_guide'] = [
            "📸 이미지 배치 가이드라인:",
            "1. 각 섹션마다 2-3문장의 설명 후 이미지 삽입",
            "2. 이미지마다 간단한 설명 텍스트 추가",
            "3. 음식 사진은 가장 맛있어 보이는 각도로 배치",
            "4. 마지막에 전체적인 분위기를 보여주는 사진으로 마무리"
        ]

        return placement_plan

    def _create_platform_specific_prompt(self, request: SnsContentGetRequest, image_analysis: Dict[str, Any],
                                         image_placement_plan: Dict[str, Any] = None) -> str:
        """
        플랫폼별 특화 프롬프트 생성
        """
        platform_spec = self.platform_specs.get(request.platform, self.platform_specs['인스타그램'])
        #tone_style = self.tone_styles.get(request.toneAndManner, {}).get(request.platform, '친근하고 자연스러운 어조')

        # 이미지 설명 추출
        image_descriptions = []
        for result in image_analysis.get('results', []):
            if 'description' in result:
                image_descriptions.append(result['description'])

        # 플랫폼별 특화 프롬프트 생성
        if request.platform == '인스타그램':
            return self._create_instagram_prompt(request, platform_spec, image_descriptions)
        elif request.platform == '네이버 블로그':
            return self._create_naver_blog_prompt(request, platform_spec, image_descriptions,
                                                  image_placement_plan)
        else:
            return self._create_instagram_prompt(request, platform_spec, image_descriptions)

    def _create_instagram_prompt(self, request: SnsContentGetRequest, platform_spec: dict,
                                 image_descriptions: list) -> str:
        """
        인스타그램 특화 프롬프트
        """
        category_hashtags = self.category_keywords.get(request.category, {}).get('인스타그램', [])

        prompt = f"""
당신은 인스타그램 마케팅 전문가입니다. 소상공인 음식점을 위한 매력적인 인스타그램 게시물을 작성해주세요.
**🍸 가게 정보:**
- 가게명: {request.storeName}
- 업종 : {request.storeType}

**🎯 콘텐츠 정보:**
- 제목: {request.title}
- 카테고리: {request.category}
- 콘텐츠 타입: {request.contentType}
- 메뉴명: {request.menuName or '특별 메뉴'}
- 이벤트: {request.eventName or '특별 이벤트'}
- 독자층: {request.target}

**📱 인스타그램 특화 요구사항:**
- 글 구조: {platform_spec['content_structure']}
- 최대 길이: {platform_spec['max_length']}자
- 해시태그: {platform_spec['hashtag_count']}개 내외

**✨ 인스타그램 작성 가이드라인:**
{chr(10).join([f"- {tip}" for tip in platform_spec['writing_tips']])}

**📸 이미지 분석 결과:**
{chr(10).join(image_descriptions) if image_descriptions else '시각적으로 매력적인 음식/매장 이미지'}

**🏷️ 추천 해시태그 카테고리:**
- 기본 해시태그: {', '.join(category_hashtags[:5])}
- 브랜딩: #우리가게이름 (실제 가게명으로 대체)
- 지역: #강남맛집 #서울카페 (실제 위치로 대체)
- 감정: #행복한시간 #맛있다 #추천해요

**💡 콘텐츠 작성 지침:**
1. 첫 문장은 반드시 관심을 끄는 후킹 문장으로 시작
2. 이모티콘을 적절히 활용하여 시각적 재미 추가
3. 스토리텔링을 통해 감정적 연결 유도
4. 명확한 행동 유도 문구 포함 (팔로우, 댓글, 저장, 방문 등)
5. 줄바꿈을 활용하여 가독성 향상
6. 해시태그는 본문과 자연스럽게 연결되도록 배치

**필수 요구사항:**
{request.requirement} or '고객의 관심을 끌고 방문을 유도하는 매력적인 게시물'

인스타그램 사용자들이 "저장하고 싶다", "친구에게 공유하고 싶다"라고 생각할 만한 매력적인 게시물을 작성해주세요.
필수 요구사항을 반드시 참고하여 작성해주세요.
"""
        return prompt

    def _create_naver_blog_prompt(self, request: SnsContentGetRequest, platform_spec: dict,
                                  image_descriptions: list, image_placement_plan: Dict[str, Any]) -> str:
        """
        네이버 블로그 특화 프롬프트 (이미지 배치 계획 포함)
        """
        category_keywords = self.category_keywords.get(request.category, {}).get('네이버 블로그', [])
        seo_keywords = platform_spec['seo_keywords']

        # 이미지 배치 정보 추가
        image_placement_info = ""
        if image_placement_plan:
            image_placement_info = f"""

**📸 이미지 배치 계획:**
{chr(10).join([f"- {section['section']}: {section['placement_guide']}" for section in image_placement_plan['structure']])}

**이미지 사용 순서:**
{chr(10).join([f"{i + 1}. {img.get('description', 'Image')} (타입: {img.get('type', '기타')})" for i, img in enumerate(image_placement_plan.get('image_sequence', []))])}
"""

        prompt = f"""
당신은 네이버 블로그 맛집 리뷰 전문가입니다. 검색 최적화와 정보 제공을 중시하는 네이버 블로그 특성에 맞는 게시물을 작성해주세요.

**🍸 가게 정보:**
- 가게명: {request.storeName}
- 업종 : {request.storeType}

**📝 콘텐츠 정보:**
- 제목: {request.title}
- 카테고리: {request.category}
- 콘텐츠 타입: {request.contentType}
- 메뉴명: {request.menuName or '대표 메뉴'}
- 이벤트: {request.eventName or '특별 이벤트'}
- 독자층: {request.target}

**🔍 네이버 블로그 특화 요구사항:**
- 글 구조: {platform_spec['content_structure']}
- 최대 길이: {platform_spec['max_length']}자
- SEO 최적화 필수

**📚 블로그 작성 가이드라인:**
{chr(10).join([f"- {tip}" for tip in platform_spec['writing_tips']])}

**🖼️ 이미지 분석 결과:**
{chr(10).join(image_descriptions) if image_descriptions else '상세한 음식/매장 정보'}

{image_placement_info}

**🔑 SEO 키워드 (자연스럽게 포함할 것):**
- 필수 키워드: {', '.join(seo_keywords[:8])}
- 카테고리 키워드: {', '.join(category_keywords[:5])}

**💡 콘텐츠 작성 지침:**
1. 검색자의 궁금증을 해결하는 정보 중심 작성
2. 구체적인 가격, 위치, 운영시간 등 실용 정보 포함
3. 개인적인 경험과 솔직한 후기 작성
4. 각 섹션마다 적절한 위치에 [IMAGE_X] 태그로 이미지 배치 위치 표시
5. 이미지마다 간단한 설명 문구 추가
6. 지역 정보와 접근성 정보 포함

**이미지 태그 사용법:**
- [IMAGE_1]: 첫 번째 이미지 배치 위치
- [IMAGE_2]: 두 번째 이미지 배치 위치  
- 각 이미지 태그 다음 줄에 이미지 설명 문구 작성

**필수 요구사항:**
{request.requirement} or '유용한 정보를 제공하여 방문을 유도하는 신뢰성 있는 후기'

네이버 검색에서 상위 노출되고, 실제로 도움이 되는 정보를 제공하는 블로그 포스트를 작성해주세요.
필수 요구사항을 반드시 참고하여 작성해주세요.
이미지 배치 위치를 [IMAGE_X] 태그로 명확히 표시해주세요.
이미지는 제공된 것만 사용하시고, 추가하진 말아주세요.
"""
        return prompt

    def _post_process_content(self, content: str, request: SnsContentGetRequest) -> str:
        """
        플랫폼별 후처리
        """
        if request.platform == '인스타그램':
            return self._post_process_instagram(content, request)
        elif request.platform == '네이버 블로그':
            return self._post_process_naver_blog(content, request)
        return content

    def _post_process_instagram(self, content: str, request: SnsContentGetRequest) -> str:
        """
        인스타그램 콘텐츠 후처리
        """
        import re

        # 해시태그 개수 조정
        hashtags = re.findall(r'#[\w가-힣]+', content)
        if len(hashtags) > 15:
            # 해시태그가 너무 많으면 중요도 순으로 15개만 유지
            all_hashtags = ' '.join(hashtags[:15])
            content = re.sub(r'#[\w가-힣]+', '', content)
            content = content.strip() + '\n\n' + all_hashtags

        # 이모티콘이 부족하면 추가
        emoji_count = content.count('😊') + content.count('🍽️') + content.count('❤️') + content.count('✨')
        if emoji_count < 3:
            content = content.replace('!', '! 😊', 1)

        return content

    def _post_process_naver_blog(self, content: str, request: SnsContentGetRequest) -> str:
        """
        네이버 블로그 콘텐츠 후처리
        """
        # 구조화된 형태로 재구성
        if '📍' not in content and '🏷️' not in content:
            # 이모티콘 기반 구조화가 없으면 추가
            lines = content.split('\n')
            structured_content = []
            for line in lines:
                if '위치' in line or '주소' in line:
                    line = f"📍 {line}"
                elif '가격' in line or '메뉴' in line:
                    line = f"🏷️ {line}"
                elif '분위기' in line or '인테리어' in line:
                    line = f"🏠 {line}"
                structured_content.append(line)
            content = '\n'.join(structured_content)

        return content

    def _format_to_html(self, content: str, request: SnsContentGetRequest,
                        image_placement_plan: Dict[str, Any] = None) -> str:
        """
        생성된 콘텐츠를 HTML 형식으로 포맷팅 (이미지 배치 포함)
        """
        # 1. literal \n 문자열을 실제 줄바꿈으로 변환
        content = content.replace('\\n', '\n')

        # 2. 인스타그램인 경우 첫 번째 이미지를 맨 위에 배치 ⭐ 새로 추가!
        images_html_content = ""
        if request.platform == '인스타그램' and request.images and len(request.images) > 0:
            # 모든 이미지를 통일된 크기로 HTML 변환 (한 줄로 작성!)
            for i, image_url in enumerate(request.images):
                # ⭐ 핵심: 모든 HTML을 한 줄로 작성해서 <br> 변환 문제 방지
                image_html = f'<div style="text-align: center; margin: 0 0 15px 0;"><img src="{image_url}" alt="이미지 {i + 1}" style="width: 100%; max-width: 500px; height: 400px; object-fit: cover; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"></div>'
                images_html_content += image_html + "\n"

            # 이미지를 콘텐츠 맨 앞에 추가
            content = images_html_content + content

        # 2. 네이버 블로그인 경우 이미지 태그를 실제 이미지로 변환
        elif request.platform == '네이버 블로그' and image_placement_plan:
            content = self._replace_image_tags_with_html(content, image_placement_plan, request.images)

        # 3. 실제 줄바꿈을 <br> 태그로 변환
        content = content.replace('\n', '<br>')

        # 4. 추가 정리: \r, 여러 공백 정리
        content = content.replace('\\r', '').replace('\r', '')

        # 6. 여러 개의 <br> 태그를 하나로 정리
        import re
        content = re.sub(r'(<br>\s*){3,}', '<br><br>', content)

        # 7. ⭐ 간단한 해시태그 스타일링 (CSS 충돌 방지)
        import re
        # style="..." 패턴을 먼저 찾아서 보호
        style_patterns = re.findall(r'style="[^"]*"', content)
        protected_content = content

        for i, pattern in enumerate(style_patterns):
            protected_content = protected_content.replace(pattern, f'___STYLE_{i}___')

        # 이제 안전하게 해시태그 스타일링
        protected_content = re.sub(r'(#[\w가-힣]+)', r'<span style="color: #1DA1F2; font-weight: bold;">\1</span>',
                                   protected_content)

        # 보호된 스타일 복원
        for i, pattern in enumerate(style_patterns):
            protected_content = protected_content.replace(f'___STYLE_{i}___', pattern)

        content = protected_content

        # 플랫폼별 헤더 스타일
        platform_style = ""
        if request.platform == '인스타그램':
            platform_style = "background: linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%);"
        elif request.platform == '네이버 블로그':
            platform_style = "background: linear-gradient(135deg, #1EC800 0%, #00B33C 100%);"
        else:
            platform_style = "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);"

        # 전체 HTML 구조
        html_content = f"""
           <div style="font-family: 'Noto Sans KR', Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 600px;">
               <div style="{platform_style} color: white; padding: 15px; border-radius: 10px 10px 0 0; text-align: center;">
                   <h3 style="margin: 0; font-size: 18px;">{request.platform} 게시물</h3>
               </div>
               <div style="background: white; padding: 20px; border-radius: 0 0 10px 10px; border: 1px solid #e1e8ed;">
                   <div style="font-size: 16px; color: #333; line-height: 1.8;">
                       {content}
                   </div>
                   {self._add_metadata_html(request)}
               </div>
           </div>
           """
        return html_content

    def _replace_image_tags_with_html(self, content: str, image_placement_plan: Dict[str, Any],
                                      image_urls: List[str]) -> str:
        """
        네이버 블로그 콘텐츠의 [IMAGE_X] 태그를 실제 이미지 HTML로 변환
        """
        import re

        # [IMAGE_X] 패턴 찾기
        image_tags = re.findall(r'\[IMAGE_(\d+)\]', content)

        for tag in image_tags:
            image_index = int(tag) - 1  # 1-based to 0-based

            if image_index < len(image_urls):
                image_url = image_urls[image_index]

                # 이미지 배치 계획에서 해당 이미지 정보 찾기
                image_info = None
                for img in image_placement_plan.get('image_sequence', []):
                    if img.get('index') == image_index:
                        image_info = img
                        break

                # 이미지 설명 생성
                image_description = ""
                if image_info:
                    description = image_info.get('description', '')
                    img_type = image_info.get('type', '기타')

                    if img_type == '음식':
                        image_description = f"😋 {description}"
                    elif img_type == '매장외관':
                        image_description = f"🏪 {description}"
                    elif img_type == '인테리어':
                        image_description = f"🏠 {description}"
                    elif img_type == '메뉴판':
                        image_description = f"📋 {description}"
                    else:
                        image_description = f"📸 {description}"

                # HTML 이미지 태그로 변환
                image_html = f"""
        <div style="text-align: center; margin: 20px 0;">
           <img src="{image_url}" alt="이미지" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
           <div style="font-size: 14px; color: #666; margin-top: 8px; font-style: italic;">
               {image_description}
           </div>
        </div>"""

                # 콘텐츠에서 태그 교체
                content = content.replace(f'[IMAGE_{tag}]', image_html)

        return content

    def _add_metadata_html(self, request: SnsContentGetRequest) -> str:
        """
        메타데이터를 HTML에 추가
        """
        metadata_html = '<div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #e1e8ed; font-size: 12px; color: #666;">'

        if request.menuName:
            metadata_html += f'<div><strong>메뉴:</strong> {request.menuName}</div>'

        if request.eventName:
            metadata_html += f'<div><strong>이벤트:</strong> {request.eventName}</div>'

        if request.startDate and request.endDate:
            metadata_html += f'<div><strong>기간:</strong> {request.startDate} ~ {request.endDate}</div>'

        metadata_html += f'<div><strong>카테고리:</strong> {request.category}</div>'
        metadata_html += f'<div><strong>플랫폼:</strong> {request.platform}</div>'
        metadata_html += f'<div><strong>생성일:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>'
        metadata_html += '</div>'

        return metadata_html
