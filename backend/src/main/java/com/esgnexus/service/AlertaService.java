package com.esgnexus.service;

import com.esgnexus.dto.AlertaDtos;
import com.esgnexus.exception.ResourceNotFoundException;
import com.esgnexus.repository.AlertaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class AlertaService {
    private final AlertaRepository repository;

    public List<AlertaDtos.AlertaResponse> listar() {
        return repository.findAll().stream().map(a -> new AlertaDtos.AlertaResponse(
                a.getId(),
                a.getFornecedor().getId(),
                a.getFornecedor().getRazaoSocial(),
                a.getTipoAlerta(),
                a.getSeveridade(),
                a.getTitulo(),
                a.getDescricao(),
                a.getStatus(),
                a.getDataCriacao().toString()
        )).toList();
    }

    public AlertaDtos.AlertaResponse resolver(Long id) {
        var alerta = repository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Alerta não encontrado"));
        alerta.setStatus("RESOLVIDO");
        var saved = repository.save(alerta);
        return new AlertaDtos.AlertaResponse(
                saved.getId(),
                saved.getFornecedor().getId(),
                saved.getFornecedor().getRazaoSocial(),
                saved.getTipoAlerta(),
                saved.getSeveridade(),
                saved.getTitulo(),
                saved.getDescricao(),
                saved.getStatus(),
                saved.getDataCriacao().toString()
        );
    }
}
