package com.esgnexus.controller;

import com.esgnexus.dto.CertificacaoDtos;
import com.esgnexus.service.CertificacaoService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/certificacoes")
@RequiredArgsConstructor
public class CertificacaoController {
    private final CertificacaoService service;

    @GetMapping
    public List<CertificacaoDtos.CertificacaoResponse> listar() { return service.listar(); }

    @PostMapping
    public CertificacaoDtos.CertificacaoResponse criar(@Valid @RequestBody CertificacaoDtos.CertificacaoRequest request) { return service.criar(request); }
}
