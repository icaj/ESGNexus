package com.esgnexus.service;

import com.esgnexus.domain.AvaliacaoFornecedor;
import com.esgnexus.domain.Fornecedor;
import com.esgnexus.dto.AvaliacaoFornecedorDtos;
import com.esgnexus.repository.AvaliacaoFornecedorRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class AvaliacaoFornecedorService {
    private final AvaliacaoFornecedorRepository repository;
    private final FornecedorService fornecedorService;
    private final ConfiguracaoService configuracaoService;

    public List<AvaliacaoFornecedorDtos.AvaliacaoResponse> listar() {
        return repository.findAllByOrderByNotaFinalDesc().stream().map(this::toResponse).toList();
    }

    public AvaliacaoFornecedorDtos.AvaliacaoResponse criar(AvaliacaoFornecedorDtos.AvaliacaoRequest request) {
        Fornecedor fornecedor = fornecedorService.buscarEntidade(request.fornecedorId());
        double pesoAmbiental = configuracaoService.obterPeso("esg.peso.ambiental", 35d);
        double pesoSocial = configuracaoService.obterPeso("esg.peso.social", 30d);
        double pesoGovernanca = configuracaoService.obterPeso("esg.peso.governanca", 35d);

        double notaFinal = (request.notaAmbiental() * pesoAmbiental + request.notaSocial() * pesoSocial + request.notaGovernanca() * pesoGovernanca) / 100.0;

        AvaliacaoFornecedor entity = AvaliacaoFornecedor.builder()
                .fornecedor(fornecedor)
                .dataAvaliacao(request.dataAvaliacao())
                .notaAmbiental(request.notaAmbiental())
                .notaSocial(request.notaSocial())
                .notaGovernanca(request.notaGovernanca())
                .notaFinal(notaFinal)
                .observacoes(request.observacoes())
                .build();

        return toResponse(repository.save(entity));
    }

    private AvaliacaoFornecedorDtos.AvaliacaoResponse toResponse(AvaliacaoFornecedor entity) {
        return new AvaliacaoFornecedorDtos.AvaliacaoResponse(
                entity.getId(),
                entity.getFornecedor().getId(),
                entity.getFornecedor().getRazaoSocial(),
                entity.getDataAvaliacao(),
                entity.getNotaAmbiental(),
                entity.getNotaSocial(),
                entity.getNotaGovernanca(),
                entity.getNotaFinal(),
                entity.getObservacoes()
        );
    }
}
