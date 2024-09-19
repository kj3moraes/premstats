"use client"

import React, { useState } from 'react';
import { Box, Container, Heading, Input, Text, InputGroup, InputRightElement, Icon, Flex, ChakraProvider, VStack, HStack, Center } from "@chakra-ui/react";
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
        <Container maxW="container.xl" py={8} height="100vh" display="flex" flexDirection="column">
          <HStack spacing={8} height="100%" alignItems="flex-start">
            {/* Left side */}
            <VStack align="stretch" width="50%" height="100%" justifyContent="center">
              <Center flexDirection="column">
                <Flex alignItems="center" mb={8}>
                  <Icon as={FaFutbol} boxSize={12} mr={4} color="black" />
                  <Heading as="h1" size="3xl" color="black">
                    premstats.xyz
                  </Heading>
                </Flex>
                <Box width="100%" maxWidth="500px">
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
                  <Text color="gray.500" fontSize="sm" mt={2} textAlign="center">
                    You can ask about any Premier League statistic up to but not including the current season
                  </Text>
                </Box>
              </Center>
            </VStack>
            {/* Right side */}
            <VStack align="stretch" width="50%" spacing={4} p={4} borderRadius="md" height="100%" overflowY="auto">
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