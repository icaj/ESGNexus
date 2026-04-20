package com.esgnexus.controller;

import com.esgnexus.dto.AvaliacaoFornecedorDtos;
import com.esgnexus.service.AvaliacaoFornecedorService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/avaliacoes")
@RequiredArgsConstructor
public class AvaliacaoFornecedorController {
    private final AvaliacaoFornecedorService service;

    @GetMapping
    public List<AvaliacaoFornecedorDtos.AvaliacaoResponse> listar() { return service.listar(); }

    @PostMapping
    public AvaliacaoFornecedorDtos.AvaliacaoResponse criar(@Valid @RequestBody AvaliacaoFornecedorDtos.AvaliacaoRequest request) { return service.criar(request); }
}
