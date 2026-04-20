package com.esgnexus.controller;

import com.esgnexus.dto.FornecedorDtos;
import com.esgnexus.service.FornecedorService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/fornecedores")
@RequiredArgsConstructor
public class FornecedorController {
    private final FornecedorService service;

    @GetMapping
    public List<FornecedorDtos.FornecedorResponse> listar() { return service.listar(); }

    @GetMapping("/{id}")
    public FornecedorDtos.FornecedorResponse buscarPorId(@PathVariable Long id) { return service.buscarPorId(id); }

    @PostMapping
    public FornecedorDtos.FornecedorResponse criar(@Valid @RequestBody FornecedorDtos.FornecedorRequest request) { return service.criar(request); }

    @PutMapping("/{id}")
    public FornecedorDtos.FornecedorResponse atualizar(@PathVariable Long id, @Valid @RequestBody FornecedorDtos.FornecedorRequest request) { return service.atualizar(id, request); }

    @DeleteMapping("/{id}")
    public void excluir(@PathVariable Long id) { service.excluir(id); }
}
