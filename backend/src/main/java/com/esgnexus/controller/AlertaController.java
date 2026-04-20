package com.esgnexus.controller;

import com.esgnexus.dto.AlertaDtos;
import com.esgnexus.service.AlertaService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/alertas")
@RequiredArgsConstructor
public class AlertaController {
    private final AlertaService service;

    @GetMapping
    public List<AlertaDtos.AlertaResponse> listar() { return service.listar(); }

    @PutMapping("/{id}/resolver")
    public AlertaDtos.AlertaResponse resolver(@PathVariable Long id) { return service.resolver(id); }
}
