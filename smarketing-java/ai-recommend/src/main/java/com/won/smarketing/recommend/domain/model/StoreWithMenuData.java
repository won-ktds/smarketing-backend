package com.won.smarketing.recommend.domain.model;

import lombok.Builder;
import lombok.Data;

import java.util.List;

@Data
@Builder
public class StoreWithMenuData {
    private StoreData storeData;
    private List<MenuData> menuDataList;
}