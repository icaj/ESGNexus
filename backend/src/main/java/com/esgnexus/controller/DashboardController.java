package com.esgnexus.controller;

import com.esgnexus.dto.DashboardDtos;
import com.esgnexus.service.DashboardService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/dashboard")
@RequiredArgsConstructor
public class DashboardController {
    private final DashboardService service;

    @GetMapping
    public DashboardDtos.DashboardResponse obterDashboard() {
        return service.obterDashboard();
    }
}
