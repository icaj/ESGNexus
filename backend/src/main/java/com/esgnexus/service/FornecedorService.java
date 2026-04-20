package com.esgnexus.service;

import com.esgnexus.domain.Fornecedor;
import com.esgnexus.dto.FornecedorDtos;
import com.esgnexus.exception.ResourceNotFoundException;
import com.esgnexus.repository.FornecedorRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class FornecedorService {
    private final FornecedorRepository repository;

    public List<FornecedorDtos.FornecedorResponse> listar() {
        return repository.findAll().stream().map(this::toResponse).toList();
    }

    public FornecedorDtos.FornecedorResponse buscarPorId(Long id) {
        return toResponse(buscarEntidade(id));
    }

    public FornecedorDtos.FornecedorResponse criar(FornecedorDtos.FornecedorRequest request) {
        Fornecedor entity = Fornecedor.builder()
                .razaoSocial(request.razaoSocial())
                .nomeFantasia(request.nomeFantasia())
                .cnpj(request.cnpj())
                .email(request.email())
                .telefone(request.telefone())
                .nomeContato(request.nomeContato())
                .segmento(request.segmento())
                .categoria(request.categoria())
                .cidade(request.cidade())
                .estado(request.estado())
                .pais(request.pais())
                .nivelRisco(request.nivelRisco())
                .status(request.status())
                .build();
        return toResponse(repository.save(entity));
    }

    public FornecedorDtos.FornecedorResponse atualizar(Long id, FornecedorDtos.FornecedorRequest request) {
        Fornecedor entity = buscarEntidade(id);
        entity.setRazaoSocial(request.razaoSocial());
        entity.setNomeFantasia(request.nomeFantasia());
        entity.setCnpj(request.cnpj());
        entity.setEmail(request.email());
        entity.setTelefone(request.telefone());
        entity.setNomeContato(request.nomeContato());
        entity.setSegmento(request.segmento());
        entity.setCategoria(request.categoria());
        entity.setCidade(request.cidade());
        entity.setEstado(request.estado());
        entity.setPais(request.pais());
        entity.setNivelRisco(request.nivelRisco());
        entity.setStatus(request.status());
        return toResponse(repository.save(entity));
    }

    public void excluir(Long id) {
        repository.delete(buscarEntidade(id));
    }

    public Fornecedor buscarEntidade(Long id) {
        return repository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Fornecedor não encontrado"));
    }

    private FornecedorDtos.FornecedorResponse toResponse(Fornecedor entity) {
        return new FornecedorDtos.FornecedorResponse(
                entity.getId(),
                entity.getRazaoSocial(),
                entity.getNomeFantasia(),
                entity.getCnpj(),
                entity.getEmail(),
                entity.getTelefone(),
                entity.getNomeContato(),
                entity.getSegmento(),
                entity.getCategoria(),
                entity.getCidade(),
                entity.getEstado(),
                entity.getPais(),
                entity.getNivelRisco(),
                entity.getStatus()
        );
    }
}
