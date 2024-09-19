"use client"

import React, { useState } from 'react';
import { Box, Container, Heading, Input, Text, InputGroup, InputRightElement, Icon, Flex, ChakraProvider, VStack, HStack } from "@chakra-ui/react";
import { ArrowForwardIcon } from "@chakra-ui/icons";
import { FaFutbol } from "react-icons/fa";
import { query_backend } from '../api/query';

export default function Home() {
  const [responses, setResponses] = useState<string[]>([]);
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    try {
      const response = await query_backend(query);
      setResponses([...responses, response]);
    } catch (error) {
      console.error('Error querying backend:', error);
      setResponses([...responses, "An error occurred while fetching the response."]);
    } finally {
      setIsLoading(false);
      setQuery('');
    }
  };

  return (
    <ChakraProvider>
      <Box as="main" minHeight="100vh" bg="white">
        <Container maxW="container.xl" py={8}>
          <HStack alignItems="flex-start" spacing={8}>
            {/* Left side */}
            <VStack align="stretch" width="50%" spacing={4}>
              <Flex alignItems="center">
                <Icon as={FaFutbol} boxSize={8} mr={2} color="black" />
                <Heading as="h1" size="2xl" color="black">
                  premstats.xyz
                </Heading>
              </Flex>
              <form onSubmit={handleSubmit}>
                <InputGroup size="lg">
                  <Input
                    pr="4.5rem"
                    placeholder="Ask about Premier League stats..."
                    _placeholder={{ color: 'gray.500' }}
                    borderColor="gray.300"
                    bg="gray.100"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    isDisabled={isLoading}
                  />
                  <InputRightElement width="4.5rem">
                    <ArrowForwardIcon
                      color={isLoading ? "gray.300" : "gray.500"}
                      boxSize={6}
                      cursor={isLoading ? "not-allowed" : "pointer"}
                      onClick={handleSubmit}
                    />
                  </InputRightElement>
                </InputGroup>
              </form>
              <Text color="gray.500" fontSize="sm">
                You can ask the system about any Premier League statistic up to but not including the current season
              </Text>
            </VStack>
            {/* Right side */}
            <VStack align="stretch" width="50%" spacing={4} p={4} borderRadius="md" minHeight="70vh">
              {responses.map((response, index) => (
                <Text key={index} color="gray.800">{response}</Text>
              ))}
              {isLoading && <Text color="gray.500">Loading...</Text>}
            </VStack>
          </HStack>
        </Container>
      </Box>
    </ChakraProvider>
  );
}