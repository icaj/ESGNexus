package com.esgnexus.controller;

import com.esgnexus.dto.ConfiguracaoDtos;
import com.esgnexus.service.ConfiguracaoService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/configuracoes")
@RequiredArgsConstructor
public class ConfiguracaoController {
    private final ConfiguracaoService service;

    @GetMapping
    public List<ConfiguracaoDtos.ConfiguracaoResponse> listar() { return service.listar(); }

    @PostMapping
    public ConfiguracaoDtos.ConfiguracaoResponse salvarOuAtualizar(@Valid @RequestBody ConfiguracaoDtos.ConfiguracaoRequest request) { return service.salvarOuAtualizar(request); }
}
