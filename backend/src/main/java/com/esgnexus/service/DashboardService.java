package com.esgnexus.service;

import com.esgnexus.dto.DashboardDtos;
import com.esgnexus.repository.AlertaRepository;
import com.esgnexus.repository.AvaliacaoFornecedorRepository;
import com.esgnexus.repository.CertificacaoRepository;
import com.esgnexus.repository.FornecedorRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class DashboardService {
    private final FornecedorRepository fornecedorRepository;
    private final AvaliacaoFornecedorRepository avaliacaoRepository;
    private final CertificacaoRepository certificacaoRepository;
    private final AlertaRepository alertaRepository;

    public DashboardDtos.DashboardResponse obterDashboard() {
        long totalFornecedores = fornecedorRepository.count();
        long totalAvaliacoes = avaliacaoRepository.count();
        long totalCertificacoes = certificacaoRepository.count();
        long alertasAbertos = alertaRepository.findAll().stream().filter(a -> "ABERTO".equalsIgnoreCase(a.getStatus())).count();
        double mediaScore = avaliacaoRepository.findAll().stream().mapToDouble(a -> a.getNotaFinal() == null ? 0.0 : a.getNotaFinal()).average().orElse(0.0);

        var top = avaliacaoRepository.findAllByOrderByNotaFinalDesc().stream().limit(10)
                .map(a -> new DashboardDtos.ItemRanking(a.getFornecedor().getId(), a.getFornecedor().getRazaoSocial(), a.getNotaFinal()))
                .toList();

        return new DashboardDtos.DashboardResponse(
                new DashboardDtos.DashboardKpis(totalFornecedores, totalAvaliacoes, totalCertificacoes, alertasAbertos, mediaScore),
                top
        );
    }
}
