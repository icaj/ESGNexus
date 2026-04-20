package com.esgnexus.service;

import com.esgnexus.domain.Certificacao;
import com.esgnexus.dto.CertificacaoDtos;
import com.esgnexus.repository.CertificacaoRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class CertificacaoService {
    private final CertificacaoRepository repository;
    private final FornecedorService fornecedorService;

    public List<CertificacaoDtos.CertificacaoResponse> listar() {
        return repository.findAll().stream().map(this::toResponse).toList();
    }

    public CertificacaoDtos.CertificacaoResponse criar(CertificacaoDtos.CertificacaoRequest request) {
        var fornecedor = fornecedorService.buscarEntidade(request.fornecedorId());
        Certificacao entity = Certificacao.builder()
                .fornecedor(fornecedor)
                .nome(request.nome())
                .orgaoEmissor(request.orgaoEmissor())
                .dataEmissao(request.dataEmissao())
                .dataValidade(request.dataValidade())
                .status(request.status())
                .urlArquivo(request.urlArquivo())
                .build();
        return toResponse(repository.save(entity));
    }

    private CertificacaoDtos.CertificacaoResponse toResponse(Certificacao entity) {
        return new CertificacaoDtos.CertificacaoResponse(
                entity.getId(),
                entity.getFornecedor().getId(),
                entity.getFornecedor().getRazaoSocial(),
                entity.getNome(),
                entity.getOrgaoEmissor(),
                entity.getDataEmissao(),
                entity.getDataValidade(),
                entity.getStatus(),
                entity.getUrlArquivo()
        );
    }
}
