package com.esgnexus.repository;

import com.esgnexus.domain.AvaliacaoFornecedor;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface AvaliacaoFornecedorRepository extends JpaRepository<AvaliacaoFornecedor, Long> {
    List<AvaliacaoFornecedor> findAllByFornecedorIdOrderByNotaFinalDesc(Long fornecedorId);
    List<AvaliacaoFornecedor> findAllByOrderByNotaFinalDesc();
}
